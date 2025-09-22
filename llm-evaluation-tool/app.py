from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize API clients
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
          'https://www.googleapis.com/auth/drive']

def get_google_sheet():
    """Get or create Google Sheet"""
    try:
        creds = Credentials.from_service_account_file(
            'credentials.json', 
            scopes=SCOPES
        )
        client = gspread.authorize(creds)
        
        try:
            sheet = client.open('llm_eval_sheet').sheet1
        except gspread.SpreadsheetNotFound:
            spreadsheet = client.create('llm_eval_sheet')
            sheet = spreadsheet.sheet1
            headers = ['Timestamp', 'Prompt', 'Model', 'Response', 
                      'Accuracy', 'Clarity', 'Creativity', 'Hallucination', 'Final Score']
            sheet.append_row(headers)
            spreadsheet.share('', perm_type='anyone', role='reader')
        
        return sheet
    except Exception as e:
        logger.error(f"Error setting up Google Sheets: {e}")
        return None

def get_gpt4_response(prompt):
    """Get response from GPT-4 with better error handling"""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            timeout=30
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = str(e)
        logger.error(f"GPT-4 Error: {error_msg}")
        
        # Return user-friendly error
        if "insufficient_quota" in error_msg or "billing" in error_msg.lower():
            return "Error: GPT-4 unavailable - API credits required. Please add billing information to your OpenAI account."
        elif "invalid_api_key" in error_msg:
            return "Error: GPT-4 authentication failed - Invalid API key"
        elif "rate_limit" in error_msg:
            return "Error: GPT-4 rate limit exceeded - Please try again in a moment"
        else:
            return f"Error: GPT-4 service error - {error_msg[:100]}"

def get_claude_response(prompt):
    """Get response from Claude with better error handling"""
    try:
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
            timeout=30
        )
        return response.content[0].text
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Claude Error: {error_msg}")
        
        # Return user-friendly error
        if "credit balance" in error_msg.lower() or "billing" in error_msg.lower():
            return "Error: Claude unavailable - API credits required. Please add credits to your Anthropic account."
        elif "authentication" in error_msg.lower() or "api_key" in error_msg.lower():
            return "Error: Claude authentication failed - Check your API key"
        elif "rate_limit" in error_msg:
            return "Error: Claude rate limit exceeded - Please try again later"
        else:
            return f"Error: Claude service error - {error_msg[:100]}"

def get_gemini_response(prompt):
    """Get response from Gemini with better error handling"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Gemini Error: {error_msg}")
        
        # Return user-friendly error
        if "404" in error_msg or "not found" in error_msg.lower():
            return "Error: Gemini model not available - Try 'gemini-1.5-flash' or check your region"
        elif "api_key" in error_msg.lower():
            return "Error: Gemini authentication failed - Check your Google API key"
        elif "quota" in error_msg.lower() or "rate" in error_msg.lower():
            return "Error: Gemini quota exceeded - You may have hit the free tier limit"
        else:
            return f"Error: Gemini service error - {error_msg[:100]}"

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/evaluate', methods=['POST'])
def evaluate_prompt():
    """Evaluate prompt across all LLMs"""
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    
    logger.info(f"Evaluating prompt: {prompt[:50]}...")
    
    # Get responses from all models (they handle their own errors)
    responses = {
        'gpt4': get_gpt4_response(prompt),
        'claude': get_claude_response(prompt),
        'gemini': get_gemini_response(prompt)
    }
    
    # Log which models succeeded/failed
    for model, response in responses.items():
        status = "❌ Error" if response.startswith("Error:") else "✅ Success"
        logger.info(f"{model}: {status}")
    
    return jsonify({'responses': responses})

@app.route('/api/submit_ratings', methods=['POST'])
def submit_ratings():
    """Submit ratings to Google Sheets"""
    data = request.json
    prompt = data.get('prompt')
    responses = data.get('responses')
    ratings = data.get('ratings')
    
    if not all([prompt, responses, ratings]):
        return jsonify({'error': 'Missing required data'}), 400
    
    sheet = get_google_sheet()
    if not sheet:
        return jsonify({'error': 'Could not access Google Sheets'}), 500
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Only save ratings for models that succeeded (not errors)
    model_names = {
        'gpt4': 'GPT-4',
        'claude': 'Claude',
        'gemini': 'Gemini'
    }
    
    saved_count = 0
    
    for model in ['gpt4', 'claude', 'gemini']:
        # Skip if this model had an error or wasn't rated
        if model not in ratings:
            logger.info(f"Skipping {model} - not rated")
            continue
            
        response_text = responses.get(model, '')
        if response_text.startswith("Error:"):
            logger.info(f"Skipping {model} - had error response")
            continue
        
        rating = ratings[model]
        row = [
            timestamp,
            prompt,
            model_names[model],
            response_text,
            rating.get('accuracy', ''),
            rating.get('clarity', ''),
            rating.get('creativity', ''),
            rating.get('hallucination', ''),
            rating.get('final', '')
        ]
        
        try:
            sheet.append_row(row)
            saved_count += 1
            logger.info(f"Saved rating for {model}")
        except Exception as e:
            logger.error(f"Error saving {model} rating: {e}")
    
    return jsonify({
        'success': True,
        'saved_count': saved_count,
        'sheet_url': sheet.spreadsheet.url
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'apis': {}
    }
    
    # Check which API keys are configured
    status['apis']['openai'] = 'configured' if os.getenv('OPENAI_API_KEY') else 'missing'
    status['apis']['anthropic'] = 'configured' if os.getenv('ANTHROPIC_API_KEY') else 'missing'
    status['apis']['google'] = 'configured' if os.getenv('GOOGLE_API_KEY') else 'missing'
    
    return jsonify(status)

if __name__ == '__main__':
    # Check for required files on startup
    if not os.path.exists('.env'):
        logger.warning("⚠️  .env file not found - API keys may be missing")
    
    if not os.path.exists('credentials.json'):
        logger.warning("⚠️  credentials.json not found - Google Sheets will not work")
    
    logger.info("🚀 Starting LLM Evaluation Tool...")
    logger.info("📝 Access at: http://localhost:5000")
    
    app.run(debug=True, port=5000)