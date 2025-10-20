# OCR Image Text Extraction API

- **Author:** MD Mutasim Billah Abu Noman Akanda 
- **Updated:** 20 October 2025

A production-ready FastAPI service that extracts text from uploaded images using Tesseract OCR. Deployed on Railway with comprehensive error handling, rate limiting, and caching.

## 📋 Deliverables

### 1. Public URL of Deployed Service
**Live API:** <https://web-production-f8dc.up.railway.app/>

### 2. API Documentation

#### HTTP Method and Endpoint
- **Method:** POST
- **Endpoint:** `/extract-text`

#### Request Format
- **Content-Type:** `multipart/form-data`
- **Field:** `image` (JPG/PNG/GIF file, max 10MB)

#### Response Format
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

#### Error Codes
- `200`: Success (health check, successful OCR)
- `400`: Bad Request (invalid file format, no content type)
- `413`: Payload Too Large (file exceeds 10MB limit)
- `422`: Unprocessable Entity (missing required field, OCR processing failed)
- `429`: Too Many Requests (rate limit exceeded)
- `500`: Internal Server Error

#### Example curl Command for Testing
```bash
curl -X POST -F "image=@test_image.jpg" https://web-production-f8dc.up.railway.app/extract-text
```

### 3. Implementation Explanation

#### OCR Service/Library Used
- **Primary OCR Engine:** Tesseract OCR (open-source)
- **Python Integration:** pytesseract library
- **Language Support:** English (tesseract-ocr-eng)
- **Alternative Considered:** Google Cloud Vision API (switched due to billing requirements)

#### File Upload and Validation
- **Upload Method:** FastAPI's `UploadFile` with `multipart/form-data`
- **File Validation:**
  - Content-type validation (MIME type checking)
  - Magic byte validation (file signature verification)
  - File size limits (10MB maximum)
  - Format validation (JPG, PNG, GIF support)
- **Security Measures:**
  - Input sanitization
  - File size enforcement
  - Format whitelist validation

#### Deployment Strategy
- **Platform:** Railway (cloud deployment platform)
- **Containerization:** Docker with Python 3.11-slim base image
- **Build Process:** Automated Docker build from GitHub repository
- **Configuration:** Environment variable handling for PORT and other settings
- **Monitoring:** Built-in health checks and logging
- **Scaling:** Automatic scaling based on demand

### 4. GitHub Repository

#### Complete Source Code
- **Repository:** <https://github.com/noman024/ocr>
- **Structure:**
  ```
  .
  ├── app/
  │   ├── __init__.py
  │   ├── main.py          # FastAPI application
  │   ├── config.py        # Configuration settings
  │   ├── models.py        # Pydantic models
  │   ├── ocr.py          # OCR service integration
  │   ├── utils.py        # Utility functions
  │   ├── rate_limit.py   # Rate limiting
  │   ├── cache.py        # Caching logic
  │   └── logging_setup.py # Logging configuration
  ├── sample_images/
  │   ├── text_sample.jpg
  │   ├── document_sample.jpg
  │   ├── low_contrast.jpg
  │   ├── mixed_content.jpg
  │   ├── no_text.jpg
  │   ├── test_gif.gif
  │   └── create_samples.py
  ├── tests/
  │   ├── __init__.py
  │   └── test_api.py
  ├── Dockerfile
  ├── requirements.txt
  ├── railway.toml
  └── README.md
  ```

#### Dockerfile
- **Base Image:** Python 3.11-slim
- **System Dependencies:** Tesseract OCR and language packs
- **Optimization:** Multi-stage build for production
- **Security:** Non-root user execution

#### README with Setup Instructions
- **Local Development:** Virtual environment setup
- **Dependencies:** Requirements installation
- **Testing:** Sample image testing
- **Deployment:** Railway deployment guide

#### Sample Test Images
- **text_sample.jpg:** Basic OCR testing
- **document_sample.jpg:** Multi-line document processing
- **low_contrast.jpg:** Edge case testing
- **mixed_content.jpg:** Complex content handling
- **no_text.jpg:** No-text scenario testing
- **test_gif.gif:** GIF format testing 
- **create_samples.py:** Image generation script

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

### Using Sample Test Images
```bash
# Basic text extraction
curl -X POST -F "image=@sample_images/text_sample.jpg" https://web-production-f8dc.up.railway.app/extract-text

# Document processing
curl -X POST -F "image=@sample_images/document_sample.jpg" https://web-production-f8dc.up.railway.app/extract-text

# Edge case testing
curl -X POST -F "image=@sample_images/no_text.jpg" https://web-production-f8dc.up.railway.app/extract-text

# Batch processing
curl -X POST -F "images=@sample_images/text_sample.jpg" -F "images=@sample_images/document_sample.jpg" https://web-production-f8dc.up.railway.app/extract-text/batch
```

### Health Check
```bash
curl https://web-production-f8dc.up.railway.app/health
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