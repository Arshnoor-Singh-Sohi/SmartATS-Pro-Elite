#!/usr/bin/env python3
"""
Setup script for SmartATS Pro
Helps with initial configuration and dependency installation
"""

import os
import sys
import subprocess
from pathlib import Path

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ['components', 'utils', 'styles']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        init_file = Path(directory) / '__init__.py'
        if not init_file.exists():
            init_file.touch()
    print("✅ Directory structure created")

def create_env_file():
    """Create .env file from .env.example if it doesn't exist"""
    if not Path('.env').exists():
        if Path('.env.example').exists():
            with open('.env.example', 'r') as example:
                content = example.read()
            
            print("\n🔑 Google Gemini API Key Setup")
            print("Get your API key from: https://makersuite.google.com/app/apikey")
            api_key = input("Enter your Google Gemini API key: ").strip()
            
            if api_key:
                content = content.replace('your_gemini_api_key_here', api_key)
                with open('.env', 'w') as env_file:
                    env_file.write(content)
                print("✅ .env file created with your API key")
            else:
                print("⚠️  No API key provided. Please update .env file manually")
        else:
            print("⚠️  .env.example not found. Please create .env file manually")
    else:
        print("✅ .env file already exists")

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies. Please run: pip install -r requirements.txt")
        return False
    return True

def download_nltk_data():
    """Download required NLTK data"""
    print("\n📚 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ NLTK data downloaded")
    except Exception as e:
        print(f"⚠️  Failed to download NLTK data: {e}")
        print("You can download it manually by running:")
        print("import nltk; nltk.download('punkt'); nltk.download('stopwords')")

def verify_setup():
    """Verify that everything is set up correctly"""
    print("\n🔍 Verifying setup...")
    
    # Check for required files
    required_files = ['app.py', 'requirements.txt', '.env']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    # Check if API key is set
    if Path('.env').exists():
        with open('.env', 'r') as f:
            content = f.read()
            if 'your_gemini_api_key_here' in content or 'GOOGLE_API_KEY=' not in content:
                print("⚠️  Google API key not properly set in .env file")
                return False
    
    print("✅ Setup verification complete")
    return True

def main():
    """Main setup function"""
    print("🚀 SmartATS Pro Setup")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Download NLTK data
    download_nltk_data()
    
    # Verify setup
    if verify_setup():
        print("\n✨ Setup complete! You can now run the application with:")
        print("   streamlit run app.py")
        print("\nThe app will open in your browser at http://localhost:8501")
    else:
        print("\n❌ Setup incomplete. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()