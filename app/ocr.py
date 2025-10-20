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
        self._check_tesseract()
        self._configure_tesseract()
    
    def _check_tesseract(self):
        """Check if Tesseract is available"""
        try:
            pytesseract.get_tesseract_version()
            logger.info("Tesseract OCR initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Tesseract not available: {e}")
            raise RuntimeError("Tesseract OCR is required but not available")
    
    def _configure_tesseract(self):
        """Configure Tesseract paths for Railway deployment"""
        import os
        import shutil
        
        # Try to find tesseract binary in common locations
        possible_paths = [
            "/usr/bin/tesseract",
            "/usr/local/bin/tesseract",
            "/nix/store/*/tesseract-*/bin/tesseract",
            shutil.which("tesseract")
        ]
        
        tesseract_path = None
        for path in possible_paths:
            if path and os.path.exists(path):
                tesseract_path = path
                break
        
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            logger.info(f"Tesseract configured at: {tesseract_path}")
        
        # Set tessdata prefix if available
        tessdata_paths = [
            "/usr/share/tesseract-ocr/4.00/tessdata",
            "/usr/share/tesseract-ocr/5/tessdata", 
            "/nix/store/*/tesseract-*/share/tessdata"
        ]
        
        for path in tessdata_paths:
            if os.path.exists(path):
                os.environ['TESSDATA_PREFIX'] = path
                logger.info(f"Tessdata configured at: {path}")
                break
    
    def extract_text(self, image_content: bytes) -> Tuple[str, float, Dict[str, Any]]:
        """
        Extract text from image using Tesseract OCR
        Returns: (text, confidence, metadata)
        """
        start_time = time.time()
        
        try:
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
            raise RuntimeError(f"OCR processing failed: {str(e)}")
    
    
    def _extract_tesseract_metadata(self, data: Dict, image: Image.Image) -> Dict[str, Any]:
        """Extract metadata from Tesseract OCR response"""
        # Count text blocks (words with confidence > 0)
        text_blocks = [i for i, conf in enumerate(data['conf']) if int(conf) > 0]
        
        metadata = {
            "text_blocks": len(text_blocks),
            "has_text": len(text_blocks) > 0,
            "tesseract_version": str(pytesseract.get_tesseract_version())
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
