import time
import logging
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .models import OCRResponse, OCRErrorResponse, BatchResponse, BatchItemResponse
from .ocr import ocr_service
from .utils import validate_image_format, validate_image_magic_bytes, get_image_metadata, calculate_file_hash
from .rate_limit import rate_limiter
from .cache import cache
from .logging_setup import configure_logging

# Configure logging
configure_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="OCR Image Text Extraction API",
    description="Extract text from images using Tesseract OCR",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_client_ip(request: Request) -> str:
    """Extract client IP from request"""
    # Check for forwarded headers first (for load balancers)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fallback to direct connection
    return request.client.host if request.client else "unknown"


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware"""
    client_ip = get_client_ip(request)
    
    # Skip rate limiting for health check
    if request.url.path == "/health":
        return await call_next(request)
    
    allowed, remaining = rate_limiter.is_allowed(client_ip)
    if not allowed:
        return JSONResponse(
            status_code=429,
            content={
                "success": False,
                "error": "Rate limit exceeded",
                "code": "RATE_LIMIT_EXCEEDED",
                "retry_after": settings.rate_limit_window_seconds
            }
        )
    
    response = await call_next(request)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Limit"] = str(settings.rate_limit_requests)
    return response


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ocr-api"}


@app.post("/extract-text", response_model=OCRResponse)
async def extract_text(
    request: Request,
    image: UploadFile = File(..., description="Image file to extract text from")
):
    """
    Extract text from uploaded image using OCR
    
    - **image**: JPG, PNG, or GIF image file (max 10MB)
    - Returns extracted text with confidence score and metadata
    """
    start_time = time.time()
    client_ip = get_client_ip(request)
    
    try:
        # Validate file
        if not image.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check file size
        if image.size and image.size > settings.max_file_size_bytes:
            raise HTTPException(
                status_code=413, 
                detail=f"File too large. Maximum size: {settings.max_file_size_bytes} bytes"
            )
        
        # Validate format
        is_valid, error_msg = validate_image_format(image)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Read file content
        content = await image.read()
        
        # Check actual file size after reading
        if len(content) > settings.max_file_size_bytes:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {settings.max_file_size_bytes} bytes"
            )
        
        # Validate magic bytes
        is_valid_magic, format_type = validate_image_magic_bytes(content)
        if not is_valid_magic:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Check cache
        file_hash = calculate_file_hash(content)
        cached_result = cache.get(file_hash)
        if cached_result:
            logger.info(f"Cache hit for file hash: {file_hash[:8]}...")
            cached_result["cached"] = True
            cached_result["processing_time_ms"] = int((time.time() - start_time) * 1000)
            return OCRResponse(**cached_result)
        
        # Extract text using OCR
        text, confidence, metadata = ocr_service.extract_text(content)
        
        # Add image metadata
        image_metadata = get_image_metadata(content)
        metadata.update(image_metadata)
        
        # Calculate processing time
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        # Prepare response
        result = {
            "success": True,
            "text": text,
            "confidence": confidence,
            "processing_time_ms": processing_time_ms,
            "metadata": metadata,
            "cached": False
        }
        
        # Cache the result
        cache.set(file_hash, result)
        
        logger.info(
            f"OCR completed for {client_ip}: {len(text)} chars, "
            f"{processing_time_ms}ms, confidence: {confidence:.2f}"
        )
        
        return OCRResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in extract_text: {e}", exc_info=True)
        processing_time_ms = int((time.time() - start_time) * 1000)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error",
                "code": "INTERNAL_ERROR",
                "processing_time_ms": processing_time_ms
            }
        )


@app.post("/extract-text/batch", response_model=BatchResponse)
async def extract_text_batch(
    request: Request,
    images: List[UploadFile] = File(..., description="Multiple image files to process")
):
    """
    Extract text from multiple uploaded images
    
    - **images**: List of JPG, PNG, or GIF image files (max 10MB each)
    - Returns results for each image with individual success/error status
    """
    start_time = time.time()
    client_ip = get_client_ip(request)
    
    if len(images) > 10:  # Limit batch size
        raise HTTPException(status_code=400, detail="Maximum 10 images per batch")
    
    results = []
    
    for i, image in enumerate(images):
        try:
            # Process each image individually
            result = await extract_text(request, image)
            results.append(BatchItemResponse(
                filename=image.filename,
                response=result,
                error=None
            ))
        except HTTPException as e:
            results.append(BatchItemResponse(
                filename=image.filename,
                response=None,
                error=OCRErrorResponse(
                    error=e.detail,
                    code="VALIDATION_ERROR"
                )
            ))
        except Exception as e:
            logger.error(f"Error processing image {i}: {e}")
            results.append(BatchItemResponse(
                filename=image.filename,
                response=None,
                error=OCRErrorResponse(
                    error="Processing failed",
                    code="PROCESSING_ERROR"
                )
            ))
    
    processing_time_ms = int((time.time() - start_time) * 1000)
    
    logger.info(f"Batch processing completed for {client_ip}: {len(images)} images, {processing_time_ms}ms")
    
    return BatchResponse(
        success=True,
        results=results,
        processing_time_ms=processing_time_ms
    )


@app.get("/cache/stats")
async def cache_stats():
    """Get cache statistics"""
    return {
        "size": cache.size(),
        "max_size": cache.max_size,
        "ttl_seconds": cache.ttl_seconds
    }


@app.delete("/cache/clear")
async def clear_cache():
    """Clear the cache"""
    cache.clear()
    return {"message": "Cache cleared successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.port)
