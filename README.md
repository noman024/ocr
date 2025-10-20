# OCR Image Text Extraction API

- **Author:** MD Mutasim Billah Abu Noman Akanda 
- **Updated:** 20 October 2025

A production-ready FastAPI service that extracts text from uploaded images using Tesseract OCR. Deployed on Railway with comprehensive error handling, rate limiting, and caching.

## 🚀 Live API

**Production URL:** <https://web-production-f8dc.up.railway.app/>

**Test Command:**
```bash
curl -X POST -F "image=@test_image.jpg" https://web-production-f8dc.up.railway.app/extract-text
```

## 📋 Requirements Met

### Core Requirements
- ✅ JPG image uploads via POST request
- ✅ OCR text extraction using Tesseract
- ✅ JSON response format
- ✅ Handle cases with no text found
- ✅ Deployed service (Railway)
- ✅ Public URL access
- ✅ Comprehensive error handling

### Technical Specifications
- **Input:** JPG/PNG/GIF files (multipart/form-data)
- **Max file size:** 10MB
- **Response format:** JSON with success, text, confidence, processing_time_ms
- **Supported formats:** JPG (primary), PNG, GIF (bonus)

### Bonus Features
- ✅ Multiple image formats (PNG, GIF)
- ✅ Confidence scores
- ✅ Rate limiting (60 requests/minute)
- ✅ Caching (SHA-256 hash-based)
- ✅ Batch processing
- ✅ Image metadata extraction

## 🔗 API Endpoints

### Extract Text
```bash
POST /extract-text
```
**Request:** `multipart/form-data` with `image` field
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
    "text_blocks": 3
  },
  "cached": false
}
```

### Batch Processing
```bash
POST /extract-text/batch
```
**Request:** Multiple `image` files (max 10 per batch)

### Health Check
```bash
GET /health
```

### Cache Management
```bash
GET /cache/stats
DELETE /cache/clear
```

## 🛠️ Implementation

### Technology Stack
- **Framework:** FastAPI
- **OCR Engine:** Tesseract OCR
- **Deployment:** Railway (Docker containerized)
- **Language:** Python 3.11

### Key Features
- **File Validation:** Content-type and magic byte validation
- **Rate Limiting:** 60 requests/minute per IP address
- **Caching:** SHA-256 hash-based with 10-minute TTL
- **Error Handling:** Comprehensive validation and error responses
- **Security:** File size limits, input sanitization

## 📊 Error Codes

- `400`: Bad Request (invalid file format, missing file)
- `413`: Payload Too Large (file exceeds 10MB limit)
- `422`: Unprocessable Entity (OCR processing failed)
- `429`: Too Many Requests (rate limit exceeded)
- `500`: Internal Server Error

## 🧪 Testing

### Health Check
```bash
curl https://web-production-f8dc.up.railway.app/health
```

### Single Image
```bash
curl -X POST -F "image=@your-image.jpg" https://web-production-f8dc.up.railway.app/extract-text
```

### Batch Processing
```bash
curl -X POST -F "images=@image1.jpg" -F "images=@image2.jpg" https://web-production-f8dc.up.railway.app/extract-text/batch
```

### Interactive Documentation
Visit: <https://web-production-f8dc.up.railway.app/docs>

## 🚀 Local Development

### Prerequisites
- Python 3.11+
- Tesseract OCR

### Setup
```bash
# Clone repository
git clone https://github.com/noman024/ocr.git
cd ocr

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Tesseract
# Ubuntu/Debian: sudo apt-get install tesseract-ocr tesseract-ocr-eng
# macOS: brew install tesseract
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki

# Run locally
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Docker
```bash
# Build and run
docker build -t ocr-api .
docker run -p 8080:8080 ocr-api
```

## 📁 Project Structure

```
app/
├── main.py          # FastAPI application
├── config.py        # Configuration settings
├── models.py        # Pydantic models
├── ocr.py          # OCR service integration
├── utils.py        # Utility functions
├── rate_limit.py   # Rate limiting
├── cache.py        # Caching logic
└── logging_setup.py # Logging configuration

Dockerfile          # Container configuration
requirements.txt    # Python dependencies
railway.toml        # Railway deployment config
```

## 🔧 Configuration

Environment variables:
- `MAX_FILE_SIZE_BYTES`: Maximum file size (default: 10485760)
- `RATE_LIMIT_REQUESTS`: Requests per window (default: 60)
- `CACHE_TTL_SECONDS`: Cache TTL (default: 600)
- `PORT`: Server port (default: 8080)

## 📈 Performance

- **Rate Limiting:** 60 requests/minute per IP
- **Caching:** Reduces processing for duplicate images
- **Batch Processing:** Up to 10 images per request
- **Response Time:** Typically < 2 seconds per image

## 🔒 Security

- File format validation (magic bytes)
- File size limits (10MB maximum)
- Rate limiting per IP address
- Input sanitization and validation
- Non-root container execution

## 📝 License

MIT License

---

**GitHub Repository:** <https://github.com/noman024/ocr> \
**Live API:** <https://web-production-f8dc.up.railway.app/> \
**API Documentation:** <https://web-production-f8dc.up.railway.app/docs>