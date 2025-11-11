#!/usr/bin/env python3
"""
Simple startup script for the Image to Text application.
"""

import os
import sys

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'flask',
        'google.generativeai',
        'openai',
        'PIL',
        'dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'PIL':
                __import__('PIL')
            elif package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package.replace('.', '_') if '.' in package else package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nPlease install dependencies by running:")
        print("  pip install -r requirements.txt")
        return False
    
    return True


def check_api_keys():
    """Check if at least one API key is configured."""
    gemini_key = os.environ.get('GEMINI_API_KEY', '')
    openai_key = os.environ.get('OPENAI_API_KEY', '')
    
    if not gemini_key and not openai_key:
        print("⚠️  Warning: No API keys found!")
        print("\nPlease set at least one of the following:")
        print("  - GEMINI_API_KEY (recommended, free tier available)")
        print("  - OPENAI_API_KEY (fallback, requires paid account)")
        print("\nYou can set them in a .env file or as environment variables.")
        print("\nGet your API keys:")
        print("  Gemini: https://makersuite.google.com/app/apikey")
        print("  OpenAI: https://platform.openai.com/api-keys")
        return False
    
    return True


if __name__ == '__main__':
    print("🚀 Starting Image to Text Application...")
    print()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check API keys
    if not check_api_keys():
        response = input("\nContinue anyway? (y/n): ").strip().lower()
        if response != 'y':
            sys.exit(1)
    
    print("✅ All checks passed!")
    print("🌐 Starting server on http://localhost:5000")
    print("📝 Press Ctrl+C to stop the server")
    print()
    
    # Import and run the app
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000)

