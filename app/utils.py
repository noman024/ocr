import hashlib
import io
from typing import Optional, Tuple
from PIL import Image
from fastapi import UploadFile


def validate_image_format(file: UploadFile) -> Tuple[bool, str]:
    """Validate image format and magic bytes"""
    if not file.content_type:
        return False, "No content type provided"
    
    # Check content type
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif"]
    if file.content_type.lower() not in allowed_types:
        return False, f"Unsupported content type: {file.content_type}"
    
    # Check file extension
    if not file.filename:
        return False, "No filename provided"
    
    ext = file.filename.lower().split('.')[-1]
    if ext not in ["jpg", "jpeg", "png", "gif"]:
        return False, f"Unsupported file extension: {ext}"
    
    return True, ""


def validate_image_magic_bytes(content: bytes) -> Tuple[bool, str]:
    """Validate image magic bytes to prevent spoofing"""
    if len(content) < 4:
        return False, "File too small"
    
    # JPEG magic bytes
    if content[:2] == b'\xff\xd8':
        return True, "jpeg"
    
    # PNG magic bytes
    if content[:8] == b'\x89PNG\r\n\x1a\n':
        return True, "png"
    
    # GIF magic bytes
    if content[:6] in [b'GIF87a', b'GIF89a']:
        return True, "gif"
    
    return False, "Invalid image format"


def get_image_metadata(content: bytes) -> dict:
    """Extract image metadata using PIL"""
    try:
        with Image.open(io.BytesIO(content)) as img:
            return {
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode,
                "has_transparency": img.mode in ("RGBA", "LA") or "transparency" in img.info
            }
    except Exception:
        return {}


def calculate_file_hash(content: bytes) -> str:
    """Calculate SHA-256 hash of file content for caching"""
    return hashlib.sha256(content).hexdigest()
