# LLM Prompt Evaluation Tool

A beautiful web-based tool to evaluate prompts across multiple LLMs (GPT-4, Claude, Gemini) and store results in Google Sheets.

## Features

- 🎨 **Modern Web UI** - Beautiful, responsive interface
- 🤖 **Multi-LLM Testing** - Test prompts across 3 major LLMs
- 📊 **Interactive Rating System** - Easy-to-use rating interface
- 📝 **Automatic Logging** - Save results to Google Sheets
- ⚡ **Real-time Updates** - Instant feedback and responses

## Project Structure

```
llm-evaluation-tool/
├── app.py                    # Flask backend
├── templates/
│   └── index.html           # Web UI (copy from artifact)
├── requirements.txt          # Python dependencies
├── .env                      # API keys (create this)
├── credentials.json          # Google service account (create this)
└── README.md                # This file
```

## Setup Instructions

### 1. Create Project Structure

```bash
mkdir llm-evaluation-tool
cd llm-evaluation-tool
mkdir templates
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get API Keys

**OpenAI (GPT-4):**
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Add to `.env` file

**Anthropic (Claude):**
1. Go to https://console.anthropic.com/settings/keys
2. Create a new API key
3. Add to `.env` file

**Google (Gemini):**
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Add to `.env` file

### 4. Setup Google Sheets Access

**Step 1: Create a Google Cloud Project**
1. Go to https://console.cloud.google.com/
2. Create a new project (or select existing)
3. Name it "LLM Evaluation Tool"

**Step 2: Enable Required APIs**
1. In your project, go to "APIs & Services" → "Enable APIs and Services"
2. Search and enable:
   - Google Sheets API
   - Google Drive API

**Step 3: Create Service Account**
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Name it "llm-eval-service-account"
4. Click "Create and Continue"
5. Skip the optional steps and click "Done"

**Step 4: Generate Credentials JSON**
1. Click on the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" → "Create New Key"
4. Select "JSON" format
5. Download the file and rename it to `credentials.json`
6. Place it in the project root directory

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
GOOGLE_API_KEY=your-google-api-key-here
```

### 6. Setup HTML Template

1. Copy the HTML UI code from the artifact
2. Save it as `templates/index.html`

## Running the Application

### Start the Flask Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Using the Web Interface

1. **Open your browser** to `http://localhost:5000`
2. **Enter your prompt** in the text area
3. **Click "Evaluate Prompt"** - The tool will query all 3 LLMs
4. **Rate each response** using the rating forms:
   - Accuracy (1-10)
   - Clarity (1-10)
   - Creativity (1-10)
   - Hallucination (yes/no)
   - Final Score (1-10)
5. **Click "Save Rating"** for each model
6. **Submit All Ratings** to save to Google Sheets

## Google Sheets Output

The sheet contains these columns:

| Timestamp | Prompt | Model | Response | Accuracy | Clarity | Creativity | Hallucination | Final Score |
|-----------|--------|-------|----------|----------|---------|------------|---------------|-------------|

## Features Showcase

### Beautiful UI
- Gradient purple background
- Smooth animations and transitions
- Responsive design for all devices
- Color-coded model badges
- Clean, modern card layout

### Smart Workflow
- Real-time loading indicators
- Validation before submission
- Success notifications
- All responses visible at once
- Easy comparison between models

### Robust Backend
- Error handling for API failures
- Automatic Google Sheets creation
- Secure credential management
- RESTful API design

## API Endpoints

### POST `/api/evaluate`
Evaluate a prompt across all LLMs

**Request:**
```json
{
  "prompt": "Explain quantum computing"
}
```

**Response:**
```json
{
  "responses": {
    "gpt4": "GPT-4 response...",
    "claude": "Claude response...",
    "gemini": "Gemini response..."
  }
}
```

### POST `/api/submit_ratings`
Submit ratings to Google Sheets

**Request:**
```json
{
  "prompt": "...",
  "responses": {...},
  "ratings": {
    "gpt4": {
      "accuracy": "8",
      "clarity": "9",
      ...
    },
    ...
  }
}
```

## Troubleshooting

**"credentials.json not found"**
- Make sure you've downloaded the service account JSON and renamed it to `credentials.json`

**"Port 5000 already in use"**
- Change the port in `app.py`: `app.run(debug=True, port=5001)`

**API errors**
- Verify all API keys are correct in `.env`
- Check that you have credits/quota for each API

**Templates not found**
- Ensure `index.html` is in the `templates/` folder
- Check that Flask can find the templates directory

**CORS errors**
- Make sure `flask-cors` is installed
- Check that CORS is enabled in `app.py`

## Production Deployment

For production deployment:

1. **Set `debug=False`** in `app.py`
2. **Use a production WSGI server** like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
3. **Set up environment variables** on your server
4. **Use HTTPS** in production
5. **Consider using** services like:
   - Heroku
   - AWS Elastic Beanstalk
   - Google Cloud Run
   - DigitalOcean App Platform

## Security Best Practices

- ✅ Never commit `.env` or `credentials.json` to version control
- ✅ Add them to `.gitignore`:
  ```
  .env
  credentials.json
  __pycache__/
  *.pyc
  ```
- ✅ Use environment variables for all sensitive data
- ✅ Rotate API keys regularly
- ✅ Limit service account permissions to only what's needed

## Advanced Features (Optional Enhancements)

### Add Rate Limiting
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/evaluate')
@limiter.limit("10 per minute")
def evaluate_prompt():
    # ...
```

### Add User Authentication
```python
from flask_login import LoginManager, login_required
# Implement user sessions
```

### Export to CSV
Add a download button to export results locally

### Batch Processing
Allow multiple prompts to be tested at once

### Comparison Charts
Add visualization comparing model performances

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - Feel free to modify and use as needed!

---

## Quick Start Commands

```bash
# Clone or create project
mkdir llm-evaluation-tool
cd llm-evaluation-tool

# Install dependencies
pip install -r requirements.txt

# Create templates folder
mkdir templates

# Copy HTML to templates/index.html
# Copy app.py to root
# Create .env with your API keys
# Download credentials.json

# Run the app
python app.py

# Open browser
# Go to http://localhost:5000
```
