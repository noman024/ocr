from pydantic import BaseModel, Field
from typing import Optional, List


class OCRResponse(BaseModel):
    success: bool = Field(True, description="Whether OCR succeeded")
    text: str = Field("", description="Extracted text content")
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    processing_time_ms: int = Field(..., ge=0)
    metadata: Optional[dict] = None
    cached: Optional[bool] = False


class OCRErrorResponse(BaseModel):
    success: bool = False
    error: str
    code: str


class BatchItemResponse(BaseModel):
    filename: Optional[str] = None
    response: Optional[OCRResponse] = None
    error: Optional[OCRErrorResponse] = None


class BatchResponse(BaseModel):
    success: bool
    results: List[BatchItemResponse]
    processing_time_ms: int
