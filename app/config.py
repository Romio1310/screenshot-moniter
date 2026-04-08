"""Application configuration."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""

    # Base directory
    BASE_DIR = Path(__file__).resolve().parent

    # Upload settings
    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER", str(BASE_DIR / "screenshots")
    )
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp"}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload

    # Logging
    LOG_DIR = os.environ.get("LOG_DIR", str(BASE_DIR / "logs"))
    LOG_FILE = "app.log"
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

    # AWS S3 (placeholder - configure via .env)
    S3_BUCKET = os.environ.get("S3_BUCKET", "screenshot-monitor-bucket")
    S3_REGION = os.environ.get("S3_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    S3_ENABLED = os.environ.get("S3_ENABLED", "false").lower() == "true"

    # Server
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 5005))
    DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
