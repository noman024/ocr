import pytest
import io
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_test_image(format="JPEG", size=(100, 100), text="Test Image"):
    """Create a test image in memory"""
    img = Image.new('RGB', size, color='white')
    # Add some text-like content
    return img


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_extract_text_no_file():
    """Test extract text without file"""
    response = client.post("/extract-text")
    assert response.status_code == 422  # Validation error


def test_extract_text_invalid_format():
    """Test extract text with invalid file format"""
    # Create a text file instead of image
    files = {"image": ("test.txt", "This is not an image", "text/plain")}
    response = client.post("/extract-text", files=files)
    assert response.status_code == 400


def test_extract_text_valid_image():
    """Test extract text with valid image"""
    # Create a test JPEG image
    img = create_test_image()
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    files = {"image": ("test.jpg", img_bytes, "image/jpeg")}
    response = client.post("/extract-text", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "text" in data
    assert "confidence" in data
    assert "processing_time_ms" in data
    assert "metadata" in data
    # Check if Tesseract metadata is present
    if "tesseract_version" in data["metadata"]:
        assert data["metadata"]["tesseract_version"] is not None


def test_batch_processing():
    """Test batch processing endpoint"""
    # Create test images
    img1 = create_test_image()
    img2 = create_test_image()
    
    img1_bytes = io.BytesIO()
    img1.save(img1_bytes, format='JPEG')
    img1_bytes.seek(0)
    
    img2_bytes = io.BytesIO()
    img2.save(img2_bytes, format='JPEG')
    img2_bytes.seek(0)
    
    files = [
        ("images", ("test1.jpg", img1_bytes, "image/jpeg")),
        ("images", ("test2.jpg", img2_bytes, "image/jpeg"))
    ]
    
    response = client.post("/extract-text/batch", files=files)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert len(data["results"]) == 2


def test_cache_stats():
    """Test cache statistics endpoint"""
    response = client.get("/cache/stats")
    assert response.status_code == 200
    data = response.json()
    assert "size" in data
    assert "max_size" in data


def test_clear_cache():
    """Test clear cache endpoint"""
    response = client.delete("/cache/clear")
    assert response.status_code == 200
    assert response.json()["message"] == "Cache cleared successfully"
