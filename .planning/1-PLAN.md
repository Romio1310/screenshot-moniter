# Phase 1 Plan — Flask Backend + API + Storage

## Plan 1-1: Project Structure + Flask App Setup

<task type="auto">
  <name>Create project structure and Flask application foundation</name>
  <files>
    app/__init__.py
    app/main.py
    app/config.py
    app/logs/.gitkeep
    app/screenshots/.gitkeep
    extension/.gitkeep
    dashboard/.gitkeep
    deployment/.gitkeep
    requirements.txt
    .gitignore
  </files>
  <action>
    1. Create the organized folder structure: app/, extension/, dashboard/, deployment/
    2. Create requirements.txt with Flask, boto3, gunicorn, python-dotenv
    3. Create app/config.py with configuration class (upload folder, log settings, allowed extensions)
    4. Create app/main.py with Flask application factory:
       - Configure logging to file (app/logs/app.log) with timestamps
       - Configure upload folder (app/screenshots/)
       - Register all routes
    5. Create .gitignore for Python project (venv, __pycache__, .env, logs)
    6. Create app/__init__.py to make it a package
  </action>
  <verify>
    - All directories exist: app/, extension/, dashboard/, deployment/
    - requirements.txt contains Flask, boto3, gunicorn
    - app/main.py imports Flask and creates app
    - .gitignore exists with proper entries
  </verify>
  <done>Project structure created with Flask app foundation</done>
</task>

## Plan 1-2: API Endpoints + Storage + Error Handling

<task type="auto">
  <name>Implement all API endpoints with storage and error handling</name>
  <files>
    app/routes.py
    app/storage.py
    app/main.py
  </files>
  <action>
    1. Create app/storage.py:
       - save_screenshot(file) → saves with timestamp filename, returns metadata
       - list_screenshots() → returns list of screenshot metadata (name, timestamp, path)
       - Validate file extensions (png, jpg, jpeg, gif, bmp)
    2. Create app/routes.py with Blueprint:
       - GET / → JSON status check (status, version, uptime, screenshot_count)
       - POST /upload → accept screenshot via multipart form, validate, store, return metadata
       - GET /screenshots → return JSON list of all screenshots with metadata
    3. Update app/main.py to register the routes blueprint
    4. Add error handling:
       - 400 for missing file in upload
       - 400 for invalid file type
       - 404 for missing resources
       - 500 for internal errors
       - All errors logged with traceback
    5. Add request logging middleware (log every API hit)
  </action>
  <verify>
    - python -c "from app.main import create_app; app = create_app(); print('OK')" succeeds
    - GET / returns JSON with status field
    - POST /upload without file returns 400
    - POST /upload with valid image returns 201
    - GET /screenshots returns JSON array
    - All actions logged to app/logs/app.log
  </verify>
  <done>All API endpoints working with storage, logging, and error handling</done>
</task>
