from flask import Flask, render_template, request, jsonify
import os
import base64
import io
from PIL import Image
import google.generativeai as genai
from openai import OpenAI
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
USE_GEMINI_FIRST = os.environ.get('USE_GEMINI_FIRST', 'true').lower() == 'true'

# Initialize Gemini if API key is available
gemini_model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-2.5-flash')
        GEMINI_AVAILABLE = True
    except Exception as e:
        print(f"Warning: Gemini initialization failed: {e}")
        GEMINI_AVAILABLE = False
        gemini_model = None
else:
    GEMINI_AVAILABLE = False

# Initialize OpenAI if API key is available
if OPENAI_API_KEY:
    try:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        OPENAI_AVAILABLE = True
    except Exception as e:
        print(f"Warning: OpenAI initialization failed: {e}")
        OPENAI_AVAILABLE = False
        openai_client = None
else:
    OPENAI_AVAILABLE = False
    openai_client = None


def image_to_base64(image_file) -> str:
    """Convert uploaded image file to base64 string."""
    image = Image.open(image_file)
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode('utf-8')


def extract_text_with_gemini(image_base64: str) -> Optional[str]:
    """Extract text from image using Gemini API."""
    if not GEMINI_AVAILABLE or not gemini_model:
        return None
    
    try:
        # Decode base64 to bytes
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        
        # Use Gemini to extract text
        response = gemini_model.generate_content([
            "Extract all text from this image. Return only the text content, no additional commentary.",
            image
        ])
        
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API error: {e}")
        return None


def extract_text_with_openai(image_base64: str) -> Optional[str]:
    """Extract text from image using OpenAI Vision API."""
    if not OPENAI_AVAILABLE or not openai_client:
        return None
    
    try:
        # OpenAI expects base64 image
        image_url = f"data:image/jpeg;base64,{image_base64}"
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract all text from this image. Return only the text content, no additional commentary."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/extract-text', methods=['POST'])
def extract_text():
    """Extract text from uploaded image."""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        # Convert image to base64
        image_base64 = image_to_base64(image_file)
        
        # Try to extract text
        text = None
        used_api = None
        
        # Try APIs based on preference
        if USE_GEMINI_FIRST and GEMINI_AVAILABLE:
            text = extract_text_with_gemini(image_base64)
            if text:
                used_api = 'Gemini'
        
        if not text and OPENAI_AVAILABLE:
            text = extract_text_with_openai(image_base64)
            if text:
                used_api = 'OpenAI'
        
        if not text and GEMINI_AVAILABLE and not USE_GEMINI_FIRST:
            text = extract_text_with_gemini(image_base64)
            if text:
                used_api = 'Gemini'
        
        if not text:
            return jsonify({
                'error': 'Failed to extract text. Please check your API keys and try again.'
            }), 500
        
        return jsonify({
            'text': text,
            'api_used': used_api
        })
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'gemini_available': GEMINI_AVAILABLE,
        'openai_available': OPENAI_AVAILABLE
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

