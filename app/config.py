import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Application
    app_name: str = "OCR Image Text Extraction API"
    version: str = "1.0.0"
    
    # File handling
    max_file_size_bytes: int = 10 * 1024 * 1024  # 10MB
    allowed_formats: List[str] = ["jpeg", "jpg", "png", "gif"]
    
    # Timeouts
    request_timeout_seconds: int = 20
    ocr_timeout_seconds: int = 15
    
    # Rate limiting
    rate_limit_requests: int = 60
    rate_limit_window_seconds: int = 60
    
    # Caching
    cache_ttl_seconds: int = 600
    cache_max_items: int = 512
    
    # Deployment
    port: int = 8080
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Handle PORT environment variable for cloud deployment
        port_env = os.getenv('PORT')
        if port_env:
            try:
                self.port = int(port_env)
            except ValueError:
                pass  # Keep default port if PORT is invalid
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
