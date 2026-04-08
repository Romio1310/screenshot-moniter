"""API routes for the Screenshot Monitoring System."""
import logging
import time
from flask import Blueprint, request, jsonify, send_from_directory

from app.config import Config
from app.storage import save_screenshot, list_screenshots

logger = logging.getLogger(__name__)

api = Blueprint("api", __name__)

# Track server start time for uptime calculation
_start_time = time.time()


@api.before_request
def log_request():
    """Log every incoming API request."""
    logger.info(
        "API HIT: %s %s [%s]",
        request.method,
        request.path,
        request.remote_addr,
    )


@api.after_request
def log_response(response):
    """Log every outgoing API response."""
    logger.info(
        "RESPONSE: %s %s → %d",
        request.method,
        request.path,
        response.status_code,
    )
    return response


# ─────────────────────────────────────────────
# GET / — System status check
# ─────────────────────────────────────────────
@api.route("/", methods=["GET"])
def status():
    """Return system status with uptime and screenshot count."""
    try:
        screenshots = list_screenshots()
        uptime_seconds = int(time.time() - _start_time)

        return jsonify({
            "status": "running",
            "version": "1.0.0",
            "uptime_seconds": uptime_seconds,
            "screenshot_count": len(screenshots),
            "message": "Intelligent Screenshot Monitoring System is operational",
        }), 200

    except Exception as e:
        logger.error("Status check failed: %s", str(e), exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


# ─────────────────────────────────────────────
# POST /upload — Accept screenshot upload
# ─────────────────────────────────────────────
@api.route("/upload", methods=["POST"])
def upload():
    """Accept a screenshot via multipart form upload."""
    try:
        # Check if file is present in request
        if "file" not in request.files:
            logger.warning("Upload attempt with no file field")
            return jsonify({
                "error": "No file field in request",
                "hint": "Send file with field name 'file'",
            }), 400

        file = request.files["file"]

        if file.filename == "":
            logger.warning("Upload attempt with empty filename")
            return jsonify({"error": "No file selected"}), 400

        # Save the screenshot
        metadata = save_screenshot(file)

        logger.info(
            "Upload successful: %s (%d bytes)",
            metadata["filename"],
            metadata["size"],
        )

        return jsonify({
            "message": "Screenshot uploaded successfully",
            "screenshot": {
                "filename": metadata["filename"],
                "original_filename": metadata["original_filename"],
                "timestamp": metadata["timestamp"],
                "size": metadata["size"],
                "url": f"/screenshots/files/{metadata['filename']}",
            },
        }), 201

    except ValueError as e:
        logger.warning("Upload validation error: %s", str(e))
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        logger.error("Upload failed: %s", str(e), exc_info=True)
        return jsonify({"error": "Internal server error during upload"}), 500


# ─────────────────────────────────────────────
# GET /screenshots — List all screenshots
# ─────────────────────────────────────────────
@api.route("/screenshots", methods=["GET"])
def screenshots():
    """Return JSON list of all stored screenshots."""
    try:
        screenshot_list = list_screenshots()

        return jsonify({
            "count": len(screenshot_list),
            "screenshots": screenshot_list,
        }), 200

    except Exception as e:
        logger.error("Failed to list screenshots: %s", str(e), exc_info=True)
        return jsonify({"error": "Failed to retrieve screenshots"}), 500


# ─────────────────────────────────────────────
# GET /screenshots/files/<filename> — Serve screenshot file
# ─────────────────────────────────────────────
@api.route("/screenshots/files/<filename>", methods=["GET"])
def serve_screenshot(filename):
    """Serve a specific screenshot file."""
    try:
        return send_from_directory(
            Config.UPLOAD_FOLDER, filename, mimetype="image/png"
        )
    except FileNotFoundError:
        logger.warning("Screenshot not found: %s", filename)
        return jsonify({"error": f"Screenshot '{filename}' not found"}), 404
    except Exception as e:
        logger.error("Failed to serve screenshot: %s", str(e), exc_info=True)
        return jsonify({"error": "Failed to serve screenshot"}), 500


# ─────────────────────────────────────────────
# Error handlers
# ─────────────────────────────────────────────
@api.app_errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logger.warning("404 Not Found: %s", request.path)
    return jsonify({"error": "Resource not found", "path": request.path}), 404


@api.app_errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    logger.warning("405 Method Not Allowed: %s %s", request.method, request.path)
    return jsonify({"error": "Method not allowed"}), 405


@api.app_errorhandler(413)
def request_too_large(error):
    """Handle file too large errors."""
    logger.warning("413 Request Too Large")
    return jsonify({
        "error": "File too large",
        "max_size_mb": Config.MAX_CONTENT_LENGTH / (1024 * 1024),
    }), 413


@api.app_errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error("500 Internal Error: %s", str(error), exc_info=True)
    return jsonify({"error": "Internal server error"}), 500
