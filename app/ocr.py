import time
import io
import logging
from typing import Tuple, Optional, Dict, Any
import pytesseract
from PIL import Image
from .config import settings

logger = logging.getLogger(__name__)


class OCRService:
    def __init__(self):
        self.tesseract_available = self._check_tesseract()
    
    def _check_tesseract(self):
        """Check if Tesseract is available"""
        try:
            pytesseract.get_tesseract_version()
            logger.info("Tesseract OCR initialized successfully")
            return True
        except Exception as e:
            logger.warning(f"Tesseract not available: {e}")
            logger.info("Running in mock mode - OCR will return placeholder text")
            return False
    
    def extract_text(self, image_content: bytes) -> Tuple[str, float, Dict[str, Any]]:
        """
        Extract text from image using Tesseract OCR
        Returns: (text, confidence, metadata)
        """
        start_time = time.time()
        
        try:
            if not self.tesseract_available:
                return self._mock_extract_text(image_content)
            
            # Load image with PIL
            image = Image.open(io.BytesIO(image_content))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Perform OCR with Tesseract
            # Get text and confidence data
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            # Extract text
            text = pytesseract.image_to_string(image).strip()
            
            # Calculate average confidence from word-level confidences
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) / 100.0 if confidences else 0.8
            
            # Extract metadata
            metadata = self._extract_tesseract_metadata(data, image)
            
            processing_time = (time.time() - start_time) * 1000
            logger.info(f"OCR completed in {processing_time:.2f}ms, text length: {len(text)}")
            
            return text, avg_confidence, metadata
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            # Fallback to mock if Tesseract fails
            return self._mock_extract_text(image_content)
    
    def _mock_extract_text(self, image_content: bytes) -> Tuple[str, float, Dict[str, Any]]:
        """Mock OCR for testing/fallback"""
        try:
            # Try to get basic image info
            with Image.open(io.BytesIO(image_content)) as img:
                width, height = img.size
                format_name = img.format or "unknown"
        except:
            width, height = 0, 0
            format_name = "unknown"
        
        # Return mock text based on image size
        if width > 1000 and height > 1000:
            mock_text = "This is a mock OCR result for a large image. In production, this would be replaced with actual text extraction from Tesseract OCR."
        elif width > 500:
            mock_text = "Mock OCR result for medium image."
        else:
            mock_text = "Small image mock text."
        
        metadata = {
            "width": width,
            "height": height,
            "format": format_name,
            "mock": True
        }
        
        return mock_text, 0.8, metadata
    
    def _extract_tesseract_metadata(self, data: Dict, image: Image.Image) -> Dict[str, Any]:
        """Extract metadata from Tesseract OCR response"""
        # Count text blocks (words with confidence > 0)
        text_blocks = [i for i, conf in enumerate(data['conf']) if int(conf) > 0]
        
        metadata = {
            "text_blocks": len(text_blocks),
            "has_text": len(text_blocks) > 0,
            "tesseract_version": str(pytesseract.get_tesseract_version()) if self.tesseract_available else "unavailable"
        }
        
        if text_blocks:
            # Get bounding boxes for text blocks
            bounding_boxes = []
            for i in text_blocks:
                if i < len(data['left']):
                    box = {
                        "x": data['left'][i],
                        "y": data['top'][i],
                        "width": data['width'][i],
                        "height": data['height'][i],
                        "text": data['text'][i],
                        "confidence": int(data['conf'][i]) / 100.0
                    }
                    bounding_boxes.append(box)
            
            metadata["bounding_boxes"] = bounding_boxes
        
        return metadata


# Global OCR service instance
ocr_service = OCRService()
