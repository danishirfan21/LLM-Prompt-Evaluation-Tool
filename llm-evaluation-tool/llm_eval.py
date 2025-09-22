import os
import gspread
from google.oauth2.service_account import Credentials
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize API clients
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
          'https://www.googleapis.com/auth/drive']

def setup_google_sheets():
    """Initialize Google Sheets connection"""
    try:
        creds = Credentials.from_service_account_file(
            'credentials.json', 
            scopes=SCOPES
        )
        client = gspread.authorize(creds)
        
        # Try to open existing sheet or create new one
        try:
            sheet = client.open('llm_eval_sheet').sheet1
            print("✓ Connected to existing 'llm_eval_sheet'")
        except gspread.SpreadsheetNotFound:
            spreadsheet = client.create('llm_eval_sheet')
            sheet = spreadsheet.sheet1
            # Set up headers
            headers = ['Timestamp', 'Prompt', 'Model', 'Response', 
                      'Accuracy', 'Clarity', 'Creativity', 'Hallucination', 'Final Score']
            sheet.append_row(headers)
            # Make sheet publicly viewable (optional)
            spreadsheet.share('', perm_type='anyone', role='reader')
            print(f"✓ Created new 'llm_eval_sheet': {spreadsheet.url}")
        
        return sheet
    except FileNotFoundError:
        print("ERROR: credentials.json not found!")
        print("Please follow the setup instructions in README.md")
        exit(1)

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

def rate_response(model_name, response):
    """Collect manual ratings for a response"""
    print(f"\n{'='*60}")
    print(f"MODEL: {model_name}")
    print(f"{'='*60}")
    print(f"RESPONSE:\n{response[:500]}{'...' if len(response) > 500 else ''}")
    print(f"{'='*60}\n")
    
    # Get ratings
    accuracy = input("Rate Accuracy (1-10): ")
    clarity = input("Rate Clarity (1-10): ")
    creativity = input("Rate Creativity (1-10): ")
    hallucination = input("Hallucination detected? (yes/no): ").lower()
    final_score = input("Final Score (1-10): ")
    
    return {
        'accuracy': accuracy,
        'clarity': clarity,
        'creativity': creativity,
        'hallucination': hallucination,
        'final_score': final_score
    }

def main():
    print("LLM PROMPT EVALUATION TOOL")
    print("="*60)
    
    # Setup Google Sheets
    sheet = setup_google_sheets()
    
    # Get user prompt
    prompt = input("\nEnter your prompt to test: ")
    
    # Define models
    models = {
        'GPT-4': get_gpt4_response,
        'Claude': get_claude_response,
        'Gemini': get_gemini_response
    }
    
    # Collect responses and ratings
    results = []
    
    for model_name, model_func in models.items():
        print(f"\n⏳ Getting response from {model_name}...")
        response = model_func(prompt)
        
        # Get manual ratings
        ratings = rate_response(model_name, response)
        
        # Store result
        result = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'prompt': prompt,
            'model': model_name,
            'response': response,
            **ratings
        }
        results.append(result)
    
    # Write to Google Sheets
    print("\n⏳ Writing results to Google Sheets...")
    for result in results:
        row = [
            result['timestamp'],
            result['prompt'],
            result['model'],
            result['response'],
            result['accuracy'],
            result['clarity'],
            result['creativity'],
            result['hallucination'],
            result['final_score']
        ]
        sheet.append_row(row)
    
    print("✓ Results successfully saved to Google Sheets!")
    print(f"\n📊 View your results: {sheet.spreadsheet.url}")

if __name__ == "__main__":
    main()