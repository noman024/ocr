# OCR Image Text Extraction API

A production-ready FastAPI-based OCR service that extracts text from uploaded images using Tesseract OCR engine. Optimized for Railway deployment with comprehensive features and robust error handling.

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
- **Railway Optimized**: Configured for Railway deployment with automatic Tesseract installation
- **Path Auto-Detection**: Automatically finds Tesseract binary in various system locations

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

## Deployment

### Railway Deployment (Recommended)

This API is optimized for Railway deployment with automatic Tesseract OCR installation.

1. **Deploy to Railway:**
   - Go to: https://railway.app
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository: `noman024/ocr`
   - Railway will automatically detect the Python app and deploy

2. **Railway Configuration:**
   - **Build System**: Nixpacks (configured in `nixpacks.toml`)
   - **Tesseract Installation**: Automatic via Nix packages
   - **Python Version**: 3.11 (specified in `runtime.txt`)
   - **Start Command**: Configured in `Procfile`

3. **Environment Variables (Optional):**
   - `MAX_FILE_SIZE_BYTES=10485760` (10MB)
   - `RATE_LIMIT_REQUESTS=60`
   - `CACHE_TTL_SECONDS=600`

### Local Development

1. **Install Tesseract:**
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-eng

# macOS
brew install tesseract

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

2. **Run locally:**
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Alternative Cloud Platforms

- **Render**: Connect GitHub repo, set build/start commands
- **Heroku**: Use included `Procfile` for deployment
- **Docker**: Use included `Dockerfile` for containerized deployment

## Testing

### Railway Deployment Testing

Once deployed to Railway, you'll get a public URL like `https://your-app-name.railway.app`

```bash
# Health check
curl https://your-app-name.railway.app/health

# Single image
curl -X POST \
  -F "image=@sample_images/text_sample.jpg" \
  https://your-app-name.railway.app/extract-text

# Batch processing
curl -X POST \
  -F "images=@sample_images/text_sample.jpg" \
  -F "images=@sample_images/document_sample.jpg" \
  https://your-app-name.railway.app/extract-text/batch

# Cache statistics
curl https://your-app-name.railway.app/cache/stats
```

### Local Testing

```bash
# Health check
curl http://localhost:8080/health

# Single image
curl -X POST \
  -F "image=@sample_images/text_sample.jpg" \
  http://localhost:8080/extract-text
```

### Using Python

```python
import requests

# Railway deployment
base_url = "https://your-app-name.railway.app"

# Health check
response = requests.get(f"{base_url}/health")
print(response.json())

# Single image
with open('sample_images/text_sample.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post(f'{base_url}/extract-text', files=files)
    print(response.json())

# Batch processing
files = []
for filename in ['text_sample.jpg', 'document_sample.jpg']:
    files.append(('images', open(f'sample_images/{filename}', 'rb')))

response = requests.post(f'{base_url}/extract-text/batch', files=files)
print(response.json())
```

### Interactive API Documentation

- **Railway**: `https://your-app-name.railway.app/docs`
- **Local**: `http://localhost:8080/docs`

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

## Railway-Specific Features

### Automatic Tesseract Configuration

The API automatically detects and configures Tesseract OCR in Railway's environment:

- **Binary Detection**: Searches common Tesseract installation paths
- **Tessdata Configuration**: Sets up language data paths
- **Fallback Mode**: Gracefully falls back to mock OCR if Tesseract unavailable
- **Logging**: Comprehensive logging for debugging deployment issues

### Railway Deployment Troubleshooting

1. **Build Failures**:
   - Check Railway logs for Nix package installation errors
   - Verify `nixpacks.toml` configuration
   - Ensure Python 3.11 compatibility

2. **Tesseract Issues**:
   - Check logs for Tesseract path configuration
   - Verify OCR service initialization
   - Test with health check endpoint

3. **Performance**:
   - Monitor Railway metrics for memory/CPU usage
   - Check rate limiting and caching statistics
   - Review processing time logs

## Support

For issues and questions:
1. Check the Railway deployment logs
2. Verify Tesseract OCR installation and configuration
3. Test with sample images provided
4. Check rate limiting and caching status
5. Review Railway metrics and performance
