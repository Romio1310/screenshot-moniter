# 📸 Intelligent Screenshot Monitor

A cross-origin, fully automated screenshot monitoring pipeline built with **Manifest V3**, **Flask**, and **Amazon S3**. 

This system consists of a Chrome Extension that silently captures the active browser tab on a configurable interval (down to every 5s) and beams the images securely to a central Flask backend. The backend can either store the images locally or ship them globally into an encrypted AWS S3 vault. Finally, a real-time web dashboard pulls the images down and displays them in a sleek, dark-mode responsive grid.

---

## 🏗 Architecture
* **Frontend:** Chrome Extension (Manifest V3 compatible, native `activeTab` integration, local storage mapping).
* **Backend:** Python / Flask (Cross-Origin Resource Sharing enabled, auto-restarting).
* **Storage Array:** AWS S3 (`boto3`) with pre-signed temporary URLs for maximum privacy, falling back to local block storage if `.env` is omitted.
* **Dashboard:** Vanilla JS/HTML dashboard with an active polling websocket-style cycle.

---

## 🚀 Quickstart (Running Locally)

### 1. The Backend
To spin up the Python server locally:
```bash
# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask Backend
export PYTHONPATH=$(pwd)
python3 -m app.main
```
Your backend APIs and Dashboard are now live at `http://localhost:5005`.

### 2. The Extension
1. Open Google Chrome and go to `chrome://extensions`.
2. Toggle **"Developer mode"** ON in the top right corner.
3. Click **"Load unpacked"** and select the `/extension` folder from this repository.
4. Pin the extension to your toolbar, open the popup, and click **Auto-Capture**.

---

## ☁️ Enabling Cloud Storage (AWS S3)

By default, screenshots are saved to the local `/app/screenshots` folder. To securely lock your photos away in Amazon S3 so they can be accessed anywhere in the world:

1. Create an AWS S3 Bucket (e.g., `screenshot-monitor-extension` in `eu-north-1`).
2. Generate an IAM User with `AmazonS3FullAccess` and grab the Access Keys.
3. Create a file in the root folder named **exactly** `.env` with the following configuration:

```env
PORT=5005
FLASK_DEBUG=false

# AWS S3 Cloud Configuration
S3_ENABLED=true
S3_REGION=eu-north-1
S3_BUCKET=your-bucket-name

AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=YourSuperSecretKey...
```
*Note: Your bucket can and should have "Block all public access" turned ON. The backend generates secure temporary pre-signed URLs to bypass the firewall so only your dashboard sees the images!*
