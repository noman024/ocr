from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_name: str = "ocr-cloud-run"
    max_file_size_bytes: int = 10 * 1024 * 1024  # 10MB
    request_timeout_seconds: int = 20
    ocr_timeout_seconds: int = 15

    # Formats
    allowed_formats: List[str] = ["jpeg", "jpg", "png", "gif"]
    # Primary requirement is JPG; PNG/GIF enabled as bonus; can be trimmed to [jpeg,jpg]

    # Rate limiting
    rate_limit_requests: int = 60
    rate_limit_window_seconds: int = 60

    # Cache TTL
    cache_ttl_seconds: int = 600
    cache_max_items: int = 512

    # Deployment
    port: int = 8080


settings = Settings()
