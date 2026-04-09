"""AWS S3 integration for screenshot cloud storage."""
import os
import logging

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from app.config import Config

logger = logging.getLogger(__name__)


def get_s3_client():
    """Create and return an S3 client."""
    try:
        if Config.AWS_ACCESS_KEY_ID and Config.AWS_SECRET_ACCESS_KEY:
            client = boto3.client(
                "s3",
                region_name=Config.S3_REGION,
                aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            )
        else:
            # Fall back to default credential chain (env vars, IAM role, etc.)
            client = boto3.client("s3", region_name=Config.S3_REGION)

        return client
    except Exception as e:
        logger.error("Failed to create S3 client: %s", str(e))
        return None


def upload_to_s3(filepath: str, filename: str) -> dict:
    """
    Upload a screenshot to S3.

    Args:
        filepath: Local path to the file
        filename: Target filename in S3

    Returns:
        dict with success status, url, and any error message
    """
    if not Config.S3_ENABLED:
        logger.info("S3 upload skipped — S3_ENABLED is false")
        return {
            "success": False,
            "skipped": True,
            "message": "S3 uploads disabled",
        }

    client = get_s3_client()
    if not client:
        return {
            "success": False,
            "error": "Failed to create S3 client",
        }

    try:
        s3_key = f"screenshots/{filename}"

        client.upload_file(
            filepath,
            Config.S3_BUCKET,
            s3_key,
            ExtraArgs={
                "ContentType": "image/png",
                "Metadata": {
                    "source": "screenshot-monitor",
                    "original-filename": filename,
                },
            },
        )

        url = f"https://{Config.S3_BUCKET}.s3.{Config.S3_REGION}.amazonaws.com/{s3_key}"

        logger.info("Uploaded to S3: %s → %s", filename, url)

        return {
            "success": True,
            "url": url,
            "bucket": Config.S3_BUCKET,
            "key": s3_key,
        }

    except NoCredentialsError:
        logger.error("S3 upload failed: No AWS credentials configured")
        return {
            "success": False,
            "error": "AWS credentials not configured",
        }

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        logger.error("S3 upload failed [%s]: %s", error_code, error_msg)
        return {
            "success": False,
            "error": f"S3 error ({error_code}): {error_msg}",
        }

    except Exception as e:
        logger.error("S3 upload failed: %s", str(e), exc_info=True)
        return {
            "success": False,
            "error": str(e),
        }


def list_s3_screenshots() -> list:
    """List all screenshots stored in S3."""
    if not Config.S3_ENABLED:
        return []

    client = get_s3_client()
    if not client:
        return []

    try:
        response = client.list_objects_v2(
            Bucket=Config.S3_BUCKET,
            Prefix="screenshots/",
        )

        screenshots = []
        for obj in response.get("Contents", []):
            if obj["Key"].endswith("/") or obj["Size"] == 0:
                continue

            # Generate a secure pre-signed URL valid for 1 hour
            presigned_url = client.generate_presigned_url(
                'get_object',
                Params={'Bucket': Config.S3_BUCKET, 'Key': obj['Key']},
                ExpiresIn=3600
            )
            
            screenshots.append({
                "filename": obj["Key"].replace("screenshots/", ""),
                "size": obj["Size"],
                "timestamp": obj["LastModified"].isoformat(),
                "url": presigned_url,
            })

        return screenshots

    except Exception as e:
        logger.error("Failed to list S3 screenshots: %s", str(e))
        return []

def delete_from_s3(filename: str) -> dict:
    """Delete a specific screenshot from S3."""
    if not Config.S3_ENABLED:
        return {"success": False, "skipped": True, "message": "S3 disabled"}

    client = get_s3_client()
    if not client:
        return {"success": False, "error": "Failed to create S3 client"}

    try:
        s3_key = f"screenshots/{filename}"
        client.delete_object(Bucket=Config.S3_BUCKET, Key=s3_key)
        logger.info("Successfully deleted S3 object: %s", s3_key)
        return {"success": True}
    except Exception as e:
        logger.error("Failed to delete from S3: %s", str(e))
        return {"success": False, "error": str(e)}
