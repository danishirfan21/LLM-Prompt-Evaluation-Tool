@echo off
echo ========================================
echo  LLM Evaluation Tool - Setup and Run
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check for .env file
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please create .env with your API keys
    echo See README.md for instructions
    pause
    exit /b 1
)

REM Check for credentials.json
if not exist "credentials.json" (
    echo WARNING: credentials.json not found!
    echo Please download Google service account credentials
    echo See README.md for instructions
    pause
    exit /b 1
)

REM Check if templates directory exists
if not exist "templates" (
    echo Creating templates directory...
    mkdir templates
    echo WARNING: Please add index.html to templates\ directory
)

REM Run the application
echo.
echo Starting Flask application...
echo Open http://localhost:5000 in your browser
echo.
python app.py

pause