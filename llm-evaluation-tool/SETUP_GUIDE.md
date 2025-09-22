# LLM Evaluation Tool - Complete Setup Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
3. [API Keys Configuration](#api-keys-configuration)
4. [Google Sheets Setup](#google-sheets-setup)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:
- ✅ Python 3.8 or higher installed
- ✅ pip (Python package manager)
- ✅ A Google account
- ✅ Credit card for API services (most have free tiers)

---

## Project Setup

### Step 1: Create Project Directory

```bash
# Create and navigate to project folder
mkdir llm-evaluation-tool
cd llm-evaluation-tool

# Create templates folder
mkdir templates
```

### Step 2: Download Project Files

Save these files to your project directory:
- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template
- `.gitignore` - Git ignore file
- `README.md` - Documentation

Save to `templates/` folder:
- `index.html` - Web interface

### Step 3: Install Dependencies

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

**On Windows:**
```batch
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

---

## API Keys Configuration

### 1. OpenAI API Key (GPT-4)

**Steps:**
1. Go to https://platform.openai.com/signup
2. Create an account or sign in
3. Navigate to https://platform.openai.com/api-keys
4. Click "Create new secret key"
5. Name it "LLM Evaluation Tool"
6. Copy the key (starts with `sk-`)
7. **Important:** Add billing info if you haven't already

**Pricing:** ~$0.03 per 1K tokens for GPT-4

---

### 2. Anthropic API Key (Claude)

**Steps:**
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to https://console.anthropic.com/settings/keys
4. Click "Create Key"
5. Name it "LLM Eval Tool"
6. Copy the key (starts with `sk-ant-`)

**Pricing:** ~$0.015 per 1K tokens for Claude

---

### 3. Google API Key (Gemini)

**Steps:**
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Select or create a Google Cloud project
5. Copy the API key

**Pricing:** Free tier available (60 requests/minute)

---

### 4. Create .env File

Create a file named `.env` in your project root:

```bash
# .env
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
GOOGLE_API_KEY=your-google-api-key-here
```

**Important:** Never commit this file to Git!

---

## Google Sheets Setup

### Step 1: Create Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Click "Select a project" → "New Project"
3. Name: "LLM Evaluation Tool"
4. Click "Create"
5. Wait for project creation (check notifications)

### Step 2: Enable Required APIs

1. In the search bar, type "Google Sheets API"
2. Click on "Google Sheets API"
3. Click "Enable"
4. Go back and search "Google Drive API"
5. Click "Enable"

### Step 3: Create Service Account

1. Navigate to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Fill in details:
   - **Name:** `llm-eval-service-account`
   - **ID:** Auto-generated (or customize)
4. Click "Create and Continue"
5. **Grant access:** Skip (click "Continue")
6. **Grant users access:** Skip (click "Done")

### Step 4: Generate Credentials JSON

1. Find your service account in the list
2. Click on the email address
3. Go to "Keys" tab
4. Click "Add Key" → "Create New Key"
5. Select "JSON" format
6. Click "Create"
7. A file downloads automatically
8. **Rename it to `credentials.json`**
9. **Move it to your project root directory**

### Step 5: Note the Service Account Email

Open `credentials.json` and find the `client_email` field:
```json
{
  "client_email": "llm-eval-service-account@your-project.iam.gserviceaccount.com"
  ...
}
```

You may need this email to share sheets manually.

---

## Running the Application

### Quick Start (Unix/Mac)

```bash
# Make run script executable
chmod +x run.sh

# Run the application
./run.sh
```

### Quick Start (Windows)

```batch
# Double-click run.bat
# OR run in command prompt:
run.bat
```

### Manual Start

```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate  # Windows

# Run Flask app
python app.py
```

### Access the Application

1. Open your browser
2. Navigate to: `http://localhost:5000`
3. You should see the beautiful gradient interface!

---

## Using the Tool

### Step-by-Step Workflow

1. **Enter Your Prompt**
   - Type or paste your test prompt in the text area
   - Example: "Explain blockchain in simple terms"

2. **Click "Evaluate Prompt"**
   - Wait for all 3 LLMs to respond (10-30 seconds)
   - Responses appear in colored cards

3. **Rate Each Response**
   - Rate on 5 metrics:
     - Accuracy (1-10)
     - Clarity (1-10)
     - Creativity (1-10)
     - Hallucination (yes/no)
     - Final Score (1-10)
   - Click "Save Rating" for each model

4. **Submit to Google Sheets**
   - Click "Submit All Ratings to Google Sheets"
   - Success message appears
   - Data is saved with timestamp

5. **View Results**
   - Check your Google Sheets
   - Sheet name: "llm_eval_sheet"
   - Analyze and compare results

---

## Troubleshooting

### Common Issues

#### "Module not found" errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

# Reinstall requirements
pip install -r requirements.txt
```

#### "credentials.json not found"
- Check file is in project root directory
- Verify filename is exactly `credentials.json`
- Ensure it's valid JSON (open in text editor)

#### API Key Errors
- Verify keys in `.env` file
- Check for extra spaces or quotes
- Ensure billing is set up for paid APIs
- Test keys individually

#### Google Sheets Permission Denied
- Sheet is auto-created on first run
- If manual sharing needed:
  1. Open the sheet
  2. Click "Share"
  3. Add the service account email
  4. Give "Editor" permissions

#### Port 5000 Already in Use
Edit `app.py`:
```python
# Change this line:
app.run(debug=True, port=5000)
# To:
app.run(debug=True, port=5001)  # Or any other port
```

#### No Responses from LLMs
- Check internet connection
- Verify API keys are correct
- Check API service status pages
- Look at Flask terminal for error messages

---

## Testing Your Setup

### Quick Test Script

Create `test_setup.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

print("Checking configuration...")
print()

# Check API keys
keys = {
    'OpenAI': os.getenv('OPENAI_API_KEY'),
    'Anthropic': os.getenv('ANTHROPIC_API_KEY'),
    'Google': os.getenv('GOOGLE_API_KEY')
}

for name, key in keys.items():
    if key:
        print(f"✓ {name} API key found")
    else:
        print(f"✗ {name} API key MISSING")

print()

# Check credentials
if os.path.exists('credentials.json'):
    print("✓ credentials.json found")
else:
    print("✗ credentials.json MISSING")

print()
print("Setup check complete!")
```

Run it:
```bash
python test_setup.py
```

---

## Next Steps

Once everything is working:

1. **Customize the UI**
   - Edit colors in `index.html`
   - Add your branding
   - Modify rating criteria

2. **Export Data**
   - Download Google Sheets as CSV
   - Analyze in Excel or Python
   - Create visualizations

3. **Scale Up**
   - Add more LLM models
   - Batch process multiple prompts
   - Create comparison charts

4. **Deploy to Production**
   - Use Heroku, AWS, or Google Cloud
   - Set up HTTPS
   - Add user authentication

---

## Additional Resources

- **OpenAI Docs:** https://platform.openai.com/docs
- **Anthropic Docs:** https://docs.anthropic.com/
- **Google AI Docs:** https://ai.google.dev/docs
- **Flask Docs:** https://flask.palletsprojects.com/
- **gspread Docs:** https://docs.gspread.org/

---

## Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review error messages in terminal
3. Verify all configuration steps
4. Check API service status pages
5. Review the README.md for updates

---

**Happy Evaluating! 🚀**