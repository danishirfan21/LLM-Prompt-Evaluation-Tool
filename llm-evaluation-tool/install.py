#!/usr/bin/env python3
"""
Interactive setup script for LLM Evaluation Tool
Guides users through the complete installation process
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_step(number, text):
    """Print step number"""
    print(f"\n{'='*60}")
    print(f"  STEP {number}: {text}")
    print(f"{'='*60}\n")

def check_python_version():
    """Ensure Python 3.8+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✓ Python version OK: {version.major}.{version.minor}.{version.micro}")

def create_directory_structure():
    """Create necessary directories"""
    print("Creating project structure...")
    
    Path("templates").mkdir(exist_ok=True)
    print("✓ Created templates/ directory")
    
    Path("static").mkdir(exist_ok=True)
    print("✓ Created static/ directory")

def check_credentials():
    """Check if credentials.json exists"""
    if not Path("credentials.json").exists():
        print("\n⚠️  credentials.json not found!")
        print("\nTo set up Google Sheets access:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a project")
        print("3. Enable Google Sheets API and Google Drive API")
        print("4. Create a Service Account")
        print("5. Download JSON key as 'credentials.json'")
        print("6. Place it in this directory")
        
        response = input("\nHave you downloaded credentials.json? (y/n): ")
        if response.lower() != 'y':
            print("\n📝 Please complete Google Cloud setup and run this script again.")
            sys.exit(1)
    else:
        print("✓ credentials.json found")
        
        # Validate JSON
        try:
            with open("credentials.json", "r") as f:
                creds = json.load(f)
                email = creds.get("client_email", "Not found")
                print(f"   Service account: {email}")
        except Exception as e:
            print(f"⚠️  Error reading credentials.json: {e}")

def setup_env_file():
    """Guide user through .env setup"""
    if Path(".env").exists():
        print("✓ .env file already exists")
        response = input("Do you want to update it? (y/n): ")
        if response.lower() != 'y':
            return
    
    print("\n📝 Let's set up your API keys...")
    print("You can get these from:")
    print("  - OpenAI: https://platform.openai.com/api-keys")
    print("  - Anthropic: https://console.anthropic.com/settings/keys")
    print("  - Google: https://makersuite.google.com/app/apikey")
    
    print("\nLeave blank to skip (you can add later)")
    
    openai_key = input("\nOpenAI API Key (sk-...): ").strip()
    anthropic_key = input("Anthropic API Key (sk-ant-...): ").strip()
    google_key = input("Google API Key: ").strip()
    
    # Create .env file
    with open(".env", "w") as f:
        f.write("# API Keys for LLM Evaluation Tool\n\n")
        f.write(f"OPENAI_API_KEY={openai_key}\n")
        f.write(f"ANTHROPIC_API_KEY={anthropic_key}\n")
        f.write(f"GOOGLE_API_KEY={google_key}\n")
    
    print("\n✓ .env file created")

def install_dependencies():
    """Install Python packages"""
    print("Installing Python dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        print("   Try running: pip install -r requirements.txt")
        sys.exit(1)

def verify_installation():
    """Verify all components are installed"""
    print("\n📋 Verifying installation...\n")
    
    issues = []
    
    # Check files
    required_files = [
        ("app.py", "Flask application"),
        ("templates/index.html", "Web interface"),
        ("requirements.txt", "Dependencies list"),
        (".env", "Environment variables"),
        ("credentials.json", "Google credentials")
    ]
    
    for file, description in required_files:
        if Path(file).exists():
            print(f"✓ {description}: {file}")
        else:
            print(f"✗ MISSING: {description} ({file})")
            issues.append(file)
    
    # Check imports
    print("\n📦 Checking Python packages...")
    packages = [
        "flask",
        "gspread",
        "openai",
        "anthropic",
        "google.generativeai"
    ]
    
    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ MISSING: {package}")
            issues.append(package)
    
    return len(issues) == 0

def create_test_file():
    """Create a test script"""
    test_content = '''#!/usr/bin/env python3
"""Quick test to verify API connections"""

import os
from dotenv import load_dotenv

load_dotenv()

print("Testing API Keys...")
print()

# Test OpenAI
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    print("✓ OpenAI client initialized")
except Exception as e:
    print(f"✗ OpenAI error: {e}")

# Test Anthropic
try:
    from anthropic import Anthropic
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    print("✓ Anthropic client initialized")
except Exception as e:
    print(f"✗ Anthropic error: {e}")

# Test Google
try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    print("✓ Google AI client initialized")
except Exception as e:
    print(f"✗ Google error: {e}")

print()
print("Test complete!")
'''
    
    with open("test_apis.py", "w") as f:
        f.write(test_content)
    
    os.chmod("test_apis.py", 0o755)
    print("✓ Created test_apis.py")

def main():
    """Main installation process"""
    print_header("🚀 LLM Evaluation Tool - Interactive Setup")
    
    print("This script will guide you through setting up the LLM Evaluation Tool.")
    print("Press Ctrl+C at any time to cancel.")
    
    input("\nPress Enter to begin...")
    
    # Step 1: Check Python
    print_step(1, "Checking Python Version")
    check_python_version()
    
    # Step 2: Create directories
    print_step(2, "Creating Project Structure")
    create_directory_structure()
    
    # Step 3: Check for required files
    print_step(3, "Checking Required Files")
    
    if not Path("app.py").exists():
        print("⚠️  app.py not found!")
        print("   Please ensure all project files are in this directory")
    
    if not Path("templates/index.html").exists():
        print("⚠️  templates/index.html not found!")
        print("   Please copy the HTML file to templates/")
    
    # Step 4: Install dependencies
    print_step(4, "Installing Dependencies")
    
    if Path("requirements.txt").exists():
        response = input("Install Python packages? (y/n): ")
        if response.lower() == 'y':
            install_dependencies()
    else:
        print("⚠️  requirements.txt not found!")
    
    # Step 5: Setup environment variables
    print_step(5, "Configuring API Keys")
    setup_env_file()
    
    # Step 6: Check Google credentials
    print_step(6, "Verifying Google Credentials")
    check_credentials()
    
    # Step 7: Create test file
    print_step(7, "Creating Test Scripts")
    create_test_file()
    
    # Step 8: Verification
    print_step(8, "Final Verification")
    
    if verify_installation():
        print("\n" + "="*60)
        print("  ✅ INSTALLATION COMPLETE!")
        print("="*60)
        print("\n📝 Next steps:")
        print("1. Test API connections: python test_apis.py")
        print("2. Start the application: python app.py")
        print("3. Open browser to: http://localhost:5000")
        print("\n📚 See README.md for detailed usage instructions")
        print("❓ See SETUP_GUIDE.md for troubleshooting")
    else:
        print("\n" + "="*60)
        print("  ⚠️  INSTALLATION INCOMPLETE")
        print("="*60)
        print("\nPlease resolve the issues above and run this script again.")
        print("See SETUP_GUIDE.md for detailed instructions.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during installation: {e}")
        sys.exit(1)