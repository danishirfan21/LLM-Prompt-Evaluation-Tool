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
        print(f"Error setting up Google Sheets: {e}")
        return None

def get_gpt4_response(prompt):
    """Get response from GPT-4"""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def get_claude_response(prompt):
    """Get response from Claude"""
    try:
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"

def get_gemini_response(prompt):
    """Get response from Gemini"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

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
    
    # Get responses from all models
    responses = {
        'gpt4': get_gpt4_response(prompt),
        'claude': get_claude_response(prompt),
        'gemini': get_gemini_response(prompt)
    }
    
    return jsonify({'responses': responses})

@app.route('/api/submit_ratings', methods=['POST'])
def submit_ratings():
    """Submit ratings to Google Sheets"""
    data = request.json
    prompt = data.get('prompt')
    responses = data.get('responses')
    ratings = data.get('ratings')
    
    sheet = get_google_sheet()
    if not sheet:
        return jsonify({'error': 'Could not access Google Sheets'}), 500
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Add each model's data as a row
    for model in ['gpt4', 'claude', 'gemini']:
        model_name = {
            'gpt4': 'GPT-4',
            'claude': 'Claude',
            'gemini': 'Gemini'
        }[model]
        
        rating = ratings.get(model, {})
        row = [
            timestamp,
            prompt,
            model_name,
            responses.get(model, ''),
            rating.get('accuracy', ''),
            rating.get('clarity', ''),
            rating.get('creativity', ''),
            rating.get('hallucination', ''),
            rating.get('final', '')
        ]
        sheet.append_row(row)
    
    return jsonify({
        'success': True,
        'sheet_url': sheet.spreadsheet.url
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)