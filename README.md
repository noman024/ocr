# OCR Image Text Extraction API

A FastAPI-based OCR service that extracts text from uploaded images using Tesseract OCR engine. Deployable locally or to any cloud platform.

## Features

- **Text Extraction**: Extract text from JPG, PNG, and GIF images
- **Tesseract OCR**: High-accuracy OCR using open-source Tesseract engine
- **Rate Limiting**: Built-in rate limiting (60 requests/minute per IP)
- **Caching**: Intelligent caching of results to improve performance
- **Batch Processing**: Process multiple images in a single request
- **Metadata Extraction**: Get image dimensions, format, and text block information
- **Error Handling**: Comprehensive error handling and validation
- **Health Checks**: Built-in health monitoring
- **Mock Mode**: Fallback to mock OCR when Tesseract is unavailable

## API Endpoints

### Extract Text from Single Image

```bash
POST /extract-text
```

**Request:**
- Content-Type: `multipart/form-data`
- Field: `image` (JPG, PNG, or GIF file, max 10MB)

**Response:**
```json
{
  "success": true,
  "text": "extracted text content here",
  "confidence": 0.95,
  "processing_time_ms": 1234,
  "metadata": {
    "width": 800,
    "height": 600,
    "format": "JPEG",
    "text_blocks": 3,
    "bounding_boxes": [...]
  },
  "cached": false
}
```

### Batch Processing
```bash
POST /extract-text/batch
```

**Request:**
- Content-Type: `multipart/form-data`
- Field: `images` (multiple image files, max 10 per batch)

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "filename": "image1.jpg",
      "response": { /* OCRResponse */ },
      "error": null
    }
  ],
  "processing_time_ms": 2500
}
```

### Health Check
```bash
GET /health
```

### Cache Management
```bash
GET /cache/stats
DELETE /cache/clear
```

## Quick Start

### Local Development

1. **Clone and setup:**
```bash
git clone <your-repo-url>
cd ocr
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Install Tesseract OCR:**
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-eng

# macOS
brew install tesseract

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

3. **Run locally:**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

4. **Test the API:**
```bash
curl -X POST -F "image=@sample_images/text_sample.jpg" http://localhost:8080/extract-text
```

### Docker

1. **Build the image:**
```bash
docker build -t ocr-api .
```

2. **Run the container:**
```bash
docker run -p 8080:8080 ocr-api
```

## Deployment Options

### Option 1: Local Deployment with Public Tunnel

1. **Install ngrok (if available):**
```bash
# Download from: https://ngrok.com/download
# Or try: sudo snap install ngrok
```

2. **Deploy locally with tunnel:**
```bash
./deploy.sh
```

### Option 2: Deploy to Railway (Recommended - Free)

1. **Create GitHub repository:**
```bash
git init
git add .
git commit -m "Initial OCR API commit"
git remote add origin https://github.com/yourusername/ocr-api.git
git push -u origin main
```

2. **Deploy to Railway:**
   - Go to: https://railway.app
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will automatically detect the Python app and deploy

3. **Set environment variables in Railway:**
   - `PORT=8080`
   - `MAX_FILE_SIZE_BYTES=10485760`

### Option 3: Deploy to Render (Free Tier)

1. **Create GitHub repository** (same as above)

2. **Deploy to Render:**
   - Go to: https://render.com
   - Sign up with GitHub
   - Click "New" → "Web Service"
   - Connect your repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Option 4: Deploy to Heroku

1. **Install Heroku CLI:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Deploy:**
```bash
heroku create your-ocr-api-name
git push heroku main
```

## Testing

### Using curl

```bash
# Single image
curl -X POST \
  -F "image=@sample_images/text_sample.jpg" \
  https://your-service-url/extract-text

# Batch processing
curl -X POST \
  -F "images=@sample_images/text_sample.jpg" \
  -F "images=@sample_images/document_sample.jpg" \
  https://your-service-url/extract-text/batch

# Health check
curl https://your-service-url/health
```

### Using Python

```python
import requests

# Single image
with open('sample_images/text_sample.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post('https://your-service-url/extract-text', files=files)
    print(response.json())

# Batch processing
files = []
for filename in ['text_sample.jpg', 'document_sample.jpg']:
    files.append(('images', open(f'sample_images/{filename}', 'rb')))

response = requests.post('https://your-service-url/extract-text/batch', files=files)
print(response.json())
```

## Configuration

The API can be configured using environment variables:

- `MAX_FILE_SIZE_BYTES`: Maximum file size (default: 10485760 = 10MB)
- `RATE_LIMIT_REQUESTS`: Requests per window (default: 60)
- `RATE_LIMIT_WINDOW_SECONDS`: Rate limit window (default: 60)
- `CACHE_TTL_SECONDS`: Cache TTL (default: 600)
- `CACHE_MAX_ITEMS`: Maximum cache items (default: 512)
- `OCR_TIMEOUT_SECONDS`: OCR processing timeout (default: 15)

## Error Codes

- `400`: Bad Request (invalid file format, missing file, etc.)
- `413`: Payload Too Large (file exceeds size limit)
- `422`: Unprocessable Entity (OCR processing failed)
- `429`: Too Many Requests (rate limit exceeded)
- `500`: Internal Server Error

## Rate Limiting

- **Limit**: 60 requests per minute per IP address
- **Headers**: `X-RateLimit-Remaining`, `X-RateLimit-Limit`
- **Response**: 429 status code when exceeded

## Caching

- **Strategy**: SHA-256 hash-based caching
- **TTL**: 10 minutes (configurable)
- **Max Items**: 512 (configurable)
- **Benefits**: Faster response times for identical images

## Monitoring and Logging

- **Structured Logging**: JSON format for Cloud Logging
- **Health Checks**: Built-in `/health` endpoint
- **Metrics**: Processing time, cache hits, error rates
- **Cloud Run**: Automatic scaling and monitoring

## Cost Optimization

- **Free Tier**: Unlimited Tesseract OCR processing
- **Cloud Run**: 2 million requests/month free
- **Caching**: Reduces OCR processing for duplicate images
- **Mock Mode**: Fallback when Tesseract OCR is unavailable

## Security

- **File Validation**: Content-type and magic byte validation
- **Size Limits**: Prevents large file uploads
- **Rate Limiting**: Prevents abuse
- **Input Sanitization**: Validates all inputs
- **Non-root Container**: Runs as non-privileged user

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/ -v
```

### Code Structure

```
app/
├── __init__.py
├── main.py          # FastAPI application
├── config.py        # Configuration settings
├── models.py        # Pydantic models
├── ocr.py          # OCR service integration
├── utils.py        # Utility functions
├── rate_limit.py   # Rate limiting
├── cache.py        # Caching logic
└── logging_setup.py # Logging configuration

tests/
├── __init__.py
└── test_api.py     # API tests

sample_images/      # Test images
Dockerfile          # Container configuration
requirements.txt    # Python dependencies
README.md          # This file
```

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
1. Check the Railway deployment logs
2. Verify Tesseract OCR installation
3. Test with sample images provided
4. Check rate limiting and caching status
