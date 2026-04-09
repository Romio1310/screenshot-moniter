"""Screenshot storage module — handles saving and listing screenshots."""
import os
import logging
from datetime import datetime, timezone
from pathlib import Path
from werkzeug.utils import secure_filename

from app.config import Config

logger = logging.getLogger(__name__)


def allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    )


def generate_filename(original_filename: str) -> str:
    """Generate a timestamp-based filename preserving the original extension."""
    ext = original_filename.rsplit(".", 1)[1].lower() if "." in original_filename else "png"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    return f"screenshot_{timestamp}.{ext}"


def save_screenshot(file) -> dict:
    """
    Save an uploaded screenshot file to the storage directory.

    Args:
        file: Werkzeug FileStorage object

    Returns:
        dict with filename, timestamp, path, size

    Raises:
        ValueError: If file is invalid or has disallowed extension
    """
    if not file or not file.filename:
        raise ValueError("No file provided")

    original_filename = secure_filename(file.filename)
    if not original_filename:
        raise ValueError("Invalid filename")

    if not allowed_file(original_filename):
        allowed = ", ".join(Config.ALLOWED_EXTENSIONS)
        raise ValueError(f"File type not allowed. Accepted types: {allowed}")

    # Ensure upload directory exists
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    # Generate timestamp-based filename
    filename = generate_filename(original_filename)
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)

    # Save the file
    file.save(filepath)
    file_size = os.path.getsize(filepath)

    timestamp = datetime.now(timezone.utc).isoformat()

    logger.info(
        "Screenshot saved: %s (%d bytes)", filename, file_size
    )

    return {
        "filename": filename,
        "original_filename": original_filename,
        "timestamp": timestamp,
        "path": filepath,
        "size": file_size,
    }


def list_screenshots() -> list:
    """
    List all screenshots in the storage directory.

    Returns:
        List of dicts with filename, timestamp, size, url
    """
    screenshots = []
    upload_dir = Path(Config.UPLOAD_FOLDER)

    if not upload_dir.exists():
        logger.warning("Upload directory does not exist: %s", Config.UPLOAD_FOLDER)
        return screenshots

    for filepath in sorted(upload_dir.iterdir(), key=lambda f: f.stat().st_mtime, reverse=True):
        if filepath.is_file() and allowed_file(filepath.name):
            stat = filepath.stat()
            screenshots.append({
                "filename": filepath.name,
                "timestamp": datetime.fromtimestamp(
                    stat.st_mtime, tz=timezone.utc
                ).isoformat(),
                "size": stat.st_size,
                "url": f"/screenshots/files/{filepath.name}",
            })

    logger.info("Listed %d screenshots", len(screenshots))
    return screenshots

def delete_local_screenshot(filename: str) -> bool:
    """Delete a specific screenshot file from local storage."""
    filepath = os.path.join(Config.UPLOAD_FOLDER, secure_filename(filename))
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info("Local screenshot deleted: %s", filepath)
            return True
        logger.warning("Local screenshot not found for deletion: %s", filepath)
        return False
    except Exception as e:
        logger.error("Failed to delete local screenshot %s: %s", filepath, str(e))
        return False
