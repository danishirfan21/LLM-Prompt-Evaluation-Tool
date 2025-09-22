# LLM Evaluation Tool - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                                 │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    Web Interface (HTML/CSS/JS)                 │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐  │  │
│  │  │   Prompt    │  │   Response  │  │   Rating Interface   │  │  │
│  │  │    Input    │  │   Display   │  │   (1-10 + yes/no)    │  │  │
│  │  └─────────────┘  └─────────────┘  └──────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ HTTP/AJAX
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      FLASK BACKEND (app.py)                          │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                               │  │
│  │  • POST /api/evaluate       - Get LLM responses                │  │
│  │  • POST /api/submit_ratings - Save to Google Sheets           │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    LLM Integration Layer                       │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │  │
│  │  │   OpenAI    │  │  Anthropic  │  │   Google    │           │  │
│  │  │   Client    │  │   Client    │  │   Client    │           │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘           │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                 Google Sheets Integration                      │  │
│  │  • gspread library                                             │  │
│  │  • Service account authentication                              │  │
│  │  • Automatic sheet creation                                    │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────┬─────────────────────────┬─────────────────────┬───────────┘
          │                         │                     │
          ▼                         ▼                     ▼
┌──────────────────┐      ┌──────────────────┐  ┌──────────────────┐
│   OpenAI API     │      │  Anthropic API   │  │   Google AI API  │
│                  │      │                  │  │                  │
│   GPT-4 Model    │      │  Claude Model    │  │  Gemini Model    │
└──────────────────┘      └──────────────────┘  └──────────────────┘
          │                         │                     │
          └─────────────────────────┴─────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Google Sheets   │
                    │                  │
                    │  llm_eval_sheet  │
                    └──────────────────┘
```

## Data Flow

### 1. Evaluation Request Flow

```
User Input (Prompt)
    │
    ▼
Frontend validates input
    │
    ▼
AJAX POST to /api/evaluate
    │
    ▼
Backend receives prompt
    │
    ├──────────────────────┬──────────────────────┐
    ▼                      ▼                      ▼
Call GPT-4 API      Call Claude API      Call Gemini API
    │                      │                      │
    ▼                      ▼                      ▼
Receive response    Receive response     Receive response
    │                      │                      │
    └──────────────────────┴──────────────────────┘
                           │
                           ▼
                  Combine responses
                           │
                           ▼
                  Return JSON to frontend
                           │
                           ▼
                  Display in UI cards
```

### 2. Rating Submission Flow

```
User rates all 3 models
    │
    ▼
Click "Submit All Ratings"
    │
    ▼
Frontend validates (all 3 rated?)
    │
    ▼
AJAX POST to /api/submit_ratings
    │
    ▼
Backend receives ratings data
    │
    ▼
Authenticate with Google Sheets
    │
    ▼
For each model (GPT-4, Claude, Gemini):
    │
    ├─── Create row with:
    │    • Timestamp
    │    • Prompt
    │    • Model name
    │    • Response text
    │    • Accuracy score
    │    • Clarity score
    │    • Creativity score
    │    • Hallucination (yes/no)
    │    • Final score
    │
    ▼
Append row to Google Sheet
    │
    ▼
Return success response
    │
    ▼
Show success message in UI
```

## Component Details

### Frontend (index.html)

**Technologies:**
- HTML5
- CSS3 (with CSS variables for theming)
- Vanilla JavaScript

**Features:**
- Responsive design
- Dark mode toggle
- Real-time validation
- Smooth animations
- AJAX communication

**Key Functions:**
```javascript
evaluatePrompt()      // Send prompt to backend
saveRating(model)     // Store rating locally
submitAllRatings()    // Send all ratings to backend
toggleTheme()         // Switch light/dark mode
```

### Backend (app.py)

**Technologies:**
- Flask (web framework)
- Python 3.8+

**Key Routes:**
```python
GET  /                    # Serve main page
POST /api/evaluate        # Process prompt
POST /api/submit_ratings  # Save to sheets
```

**API Client Initialization:**
```python
OpenAI(api_key=...)           # GPT-4
Anthropic(api_key=...)        # Claude
genai.configure(api_key=...)  # Gemini
```

### External Services

#### 1. LLM APIs

**OpenAI (GPT-4)**
- Model: `gpt-4`
- Max tokens: 500
- Rate limits: Apply

**Anthropic (Claude)**
- Model: `claude-3-5-sonnet-20241022`
- Max tokens: 500
- Rate limits: Apply

**Google (Gemini)**
- Model: `gemini-pro`
- Default settings
- Free tier available

#### 2. Google Sheets

**Authentication:**
- Service account with JSON credentials
- OAuth 2.0 scopes for Sheets and Drive

**Operations:**
- Create spreadsheet (first run)
- Append rows (each submission)
- Share with public read access

## Security Considerations

### API Keys
- ✅ Stored in `.env` file (not in code)
- ✅ Never committed to version control
- ✅ Loaded via `python-dotenv`

### Google Credentials
- ✅ Service account (not user OAuth)
- ✅ Minimal required permissions
- ✅ JSON file excluded from Git

### Web Security
- ✅ CORS enabled for development
- ⚠️ Should add HTTPS in production
- ⚠️ Should add rate limiting for production
- ⚠️ Should add user authentication for production

## Scalability Considerations

### Current Architecture (Development)
- Single Flask process
- Synchronous API calls
- No caching
- No queue system

### Production Recommendations

**For High Traffic:**
```
┌─────────────┐
│   Nginx     │  ← Reverse proxy
│   (80/443)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Gunicorn   │  ← WSGI server (4-8 workers)
│  (5000)     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Flask     │  ← Application
│   App       │
└──────┬──────┘
       │
       ├──────────┐
       ▼          ▼
   ┌─────┐    ┌──────┐
   │Redis│    │Celery│  ← Async task queue
   │Cache│    │Queue │
   └─────┘    └──────┘
```

**Improvements:**
1. **Caching**: Redis for API responses
2. **Async**: Celery for LLM calls
3. **Load Balancing**: Multiple app instances
4. **Database**: PostgreSQL for history
5. **CDN**: Static asset delivery

## File Structure

```
llm-evaluation-tool/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (SECRET)
├── credentials.json       # Google credentials (SECRET)
├── .gitignore            # Git ignore rules
├── README.md             # Main documentation
├── SETUP_GUIDE.md        # Detailed setup instructions
├── ARCHITECTURE.md       # This file
│
├── templates/            # HTML templates
│   └── index.html       # Main web interface
│
├── static/              # Static assets (optional)
│   ├── css/
│   ├── js/
│   └── images/
│
├── scripts/             # Utility scripts
│   ├── install.py      # Interactive installer
│   ├── test_apis.py    # API connection tester
│   ├── run.sh          # Unix start script
│   └── run.bat         # Windows start script
│
└── venv/               # Virtual environment (not in git)
```

## Environment Variables

Required variables in `.env`:

```bash
# LLM API Keys
OPENAI_API_KEY=sk-...          # OpenAI GPT-4
ANTHROPIC_API_KEY=sk-ant-...   # Anthropic Claude
GOOGLE_API_KEY=...             # Google Gemini

# Optional: Flask Configuration
FLASK_ENV=development          # development/production
FLASK_DEBUG=True              # Enable debug mode
SECRET_KEY=...                # Flask secret key

# Optional: Server Configuration
PORT=5000                     # Server port
HOST=0.0.0.0                 # Server host
```

## Database Schema (Google Sheets)

### Sheet: llm_eval_sheet

| Column       | Type   | Description                    |
|-------------|--------|--------------------------------|
| Timestamp   | String | ISO format datetime            |
| Prompt      | String | User's input prompt            |
| Model       | String | Model name (GPT-4/Claude/Gemini) |
| Response    | String | Model's full response text     |
| Accuracy    | Number | Rating 1-10                    |
| Clarity     | Number | Rating 1-10                    |
| Creativity  | Number | Rating 1-10                    |
| Hallucination | String | "yes" or "no"                 |
| Final Score | Number | Overall rating 1-10            |

**Example Row:**
```
2025-09-22 14:30:15 | "Explain AI" | GPT-4 | "Artificial Intelligence is..." | 9 | 8 | 7 | no | 8
```

## API Documentation

### POST /api/evaluate

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
    "gpt4": "Quantum computing uses quantum bits...",
    "claude": "Quantum computers leverage quantum mechanics...",
    "gemini": "In quantum computing, information is stored..."
  }
}
```

**Error Response:**
```json
{
  "error": "No prompt provided"
}
```

### POST /api/submit_ratings

**Request:**
```json
{
  "prompt": "Explain quantum computing",
  "responses": {
    "gpt4": "...",
    "claude": "...",
    "gemini": "..."
  },
  "ratings": {
    "gpt4": {
      "accuracy": "9",
      "clarity": "8",
      "creativity": "7",
      "hallucination": "no",
      "final": "8"
    },
    "claude": { ... },
    "gemini": { ... }
  }
}
```

**Success Response:**
```json
{
  "success": true,
  "sheet_url": "https://docs.google.com/spreadsheets/d/..."
}
```

**Error Response:**
```json
{
  "error": "Could not access Google Sheets"
}
```

## Performance Metrics

### Typical Response Times

| Operation              | Time    | Notes                    |
|-----------------------|---------|--------------------------|
| Page Load             | < 1s    | Initial HTML/CSS/JS      |
| LLM API Calls (total) | 5-15s   | 3 parallel requests      |
| - GPT-4              | 2-5s    | Varies by load           |
| - Claude             | 2-5s    | Usually fastest          |
| - Gemini             | 1-3s    | Free tier              |
| Google Sheets Write   | 1-2s    | Per submission           |
| Total Workflow        | 6-20s   | Prompt to saved results  |

### API Cost Estimates

**Per Evaluation (3 models, 500 tokens each):**
- GPT-4: ~$0.015
- Claude: ~$0.008
- Gemini: Free (up to limits)
- **Total: ~$0.023 per evaluation**

**Monthly Costs (1000 evaluations):**
- ~$23/month for heavy usage
- Most users: $5-10/month

## Deployment Options

### 1. Local Development
```bash
python app.py
# Runs on http://localhost:5000
```

### 2. Heroku
```bash
# Add Procfile
web: gunicorn app:app

# Deploy
heroku create llm-eval-tool
git push heroku main
```

### 3. Google Cloud Run
```bash
# Build container
gcloud builds submit --tag gcr.io/PROJECT_ID/llm-eval

# Deploy
gcloud run deploy --image gcr.io/PROJECT_ID/llm-eval
```

### 4. AWS Elastic Beanstalk
```bash
eb init -p python-3.11 llm-eval-tool
eb create llm-eval-env
eb deploy
```

### 5. DigitalOcean App Platform
- Connect GitHub repository
- Auto-deploy on push
- Managed infrastructure

## Monitoring & Logging

### Recommended Additions

**Application Monitoring:**
- Sentry for error tracking
- New Relic for performance
- DataDog for metrics

**Logging:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

**Metrics to Track:**
- API response times
- Error rates per LLM
- User evaluation counts
- Cost per evaluation
- Sheet write success rate

## Future Enhancements

### Planned Features

1. **User Authentication**
   - Login/signup system
   - Personal evaluation history
   - Team collaboration

2. **Advanced Analytics**
   - Model comparison charts
   - Performance trends over time
   - Statistical analysis
   - Export to CSV/Excel

3. **Batch Processing**
   - Upload CSV of prompts
   - Queue system for large batches
   - Progress tracking

4. **More Models**
   - Llama 2/3
   - Mistral
   - Cohere
   - Custom models

5. **Custom Metrics**
   - User-defined rating criteria
   - Domain-specific evaluations
   - Weighted scoring

6. **Collaboration**
   - Share evaluations
   - Comments and discussions
   - Team workspaces

7. **API Access**
   - RESTful API for integrations
   - Webhooks for automation
   - SDK for developers

## Testing Strategy

### Unit Tests
```python
# tests/test_app.py
def test_evaluate_endpoint():
    response = client.post('/api/evaluate', 
                          json={'prompt': 'test'})
    assert response.status_code == 200
    assert 'responses' in response.json
```

### Integration Tests
- Mock LLM APIs
- Test Google Sheets integration
- End-to-end workflow tests

### Load Testing
```bash
# Using locust
locust -f locustfile.py --host=http://localhost:5000
```

## Troubleshooting Guide

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| 500 Error | Missing API keys | Check `.env` file |
| API timeout | Slow LLM response | Increase timeout limits |
| Sheet permission denied | Wrong credentials | Verify service account |
| Import errors | Missing packages | `pip install -r requirements.txt` |
| Port in use | Another app on 5000 | Change port in app.py |

## Contributing Guidelines

### Development Setup
1. Fork repository
2. Create feature branch
3. Install dev dependencies
4. Write tests
5. Submit pull request

### Code Style
- PEP 8 for Python
- ESLint for JavaScript
- Prettier for formatting

---

## Architecture Decision Records

### ADR 001: Flask vs FastAPI
**Decision**: Use Flask
**Rationale**: 
- Simpler for beginners
- Excellent ecosystem
- Synchronous is fine for this use case

### ADR 002: Google Sheets vs Database
**Decision**: Use Google Sheets
**Rationale**:
- Easy setup
- No server maintenance
- Familiar interface for users
- Easy data export

### ADR 003: Frontend Framework
**Decision**: Vanilla JavaScript
**Rationale**:
- No build step
- Faster development
- Easier for contributors
- Sufficient for current needs

---

**Version**: 1.0.0  
**Last Updated**: September 2025  
**Maintainer**: Your Team