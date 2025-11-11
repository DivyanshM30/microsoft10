# Image to Text Converter

A modern web application that extracts text from images using AI. Supports Gemini API (primary) and OpenAI Vision API (fallback).

## Features

- 🖼️ Upload images via click or drag & drop
- 🤖 Multiple AI backend support (Gemini and OpenAI)
- 🎨 Modern, responsive UI
- 📋 Copy extracted text to clipboard
- 🔄 Automatic fallback between APIs
- ⚡ Fast and efficient text extraction

## Prerequisites

- Python 3.8 or higher
- API key from one of the following:
  - **Gemini API** (Recommended - Free tier available): Get your key from [Google AI Studio](https://makersuite.google.com/app/apikey)
  - **OpenAI API** (Fallback): Get your key from [OpenAI Platform](https://platform.openai.com/api-keys)

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:

   Create a `.env` file in the project root (or set environment variables):
   
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   USE_GEMINI_FIRST=true
   ```

   **Note:** You only need at least one API key. The app will use Gemini by default if available, and fall back to OpenAI if Gemini fails or is not configured.

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up your API key(s):**

   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   # Optional: Add OpenAI key as fallback
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   Or set environment variables directly:
   ```bash
   # Windows (PowerShell)
   $env:GEMINI_API_KEY="your_key_here"
   
   # Linux/Mac
   export GEMINI_API_KEY="your_key_here"
   ```

3. **Start the server:**
```bash
python app.py
```
   Or use the startup script with checks:
```bash
python run.py
```

4. **Open your browser:**
   Navigate to `http://localhost:5000`

5. **Use the app:**
   - Upload an image (click or drag & drop)
   - Click "Extract Text"
   - Copy the extracted text using the "Copy to Clipboard" button

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Upload an image (click or drag & drop)

4. Click "Extract Text" to get the text from the image

5. Copy the extracted text using the "Copy to Clipboard" button

## API Options

### Gemini API (Recommended - Free!)
- **Pros:** Free tier available (generous limits), good performance, reliable, no credit card required
- **Cons:** Requires Google account
- **Get API Key:** [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Cost:** Free for most use cases

### OpenAI Vision API (Fallback)
- **Pros:** Very accurate, supports multiple models, excellent OCR quality
- **Cons:** Requires paid API key (pay-as-you-go, ~$0.01-0.03 per image)
- **Get API Key:** [OpenAI Platform](https://platform.openai.com/api-keys)
- **Model Used:** gpt-4o (multimodal model)
- **Cost:** Pay-as-you-go pricing

### Alternative Free Option: Tesseract OCR (Optional)
If you want a completely free, local option that doesn't require API keys, you can add Tesseract OCR support:
- **Pros:** Completely free, works offline, no API keys needed
- **Cons:** Less accurate than AI models, requires system installation
- **Installation:** Follow [Tesseract installation guide](https://github.com/tesseract-ocr/tesseract)
- **Note:** This would require additional code changes to integrate

## Configuration

You can control which API to use first by setting the `USE_GEMINI_FIRST` environment variable:
- `USE_GEMINI_FIRST=true` (default): Try Gemini first, fallback to OpenAI
- `USE_GEMINI_FIRST=false`: Try OpenAI first, fallback to Gemini

## Supported Image Formats

- JPEG/JPG
- PNG
- GIF
- WebP

## Troubleshooting

### "Failed to extract text" error
- Check that at least one API key is set correctly
- Verify your API keys are valid and have credits/quota
- Check the console for detailed error messages

### Gemini API not working
- The app will automatically fallback to OpenAI if configured
- Check your Gemini API key is correct
- Verify you have access to the Gemini API

### OpenAI API not working
- Check your API key is correct
- Verify you have credits in your OpenAI account
- Check that the model `gpt-4o` is available to your account

## Health Check

You can check the status of available APIs by visiting:
```
http://localhost:5000/health
```

This will show which APIs are configured and available.

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

