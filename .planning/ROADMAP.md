# Roadmap — Intelligent Screenshot Monitoring System

## Milestone: v1.0

### Phase 1: Flask Backend + API + Storage
**Goal:** Stand up the Flask backend with all API endpoints, local screenshot storage, comprehensive logging, and organized project structure.

**Requirements:** BE-01, BE-02, BE-03, BE-04, BE-05, SS-01, SS-02, SS-03, DP-04

**Success Criteria:**
1. `GET /` returns JSON status with uptime
2. `POST /upload` accepts image file and stores it with timestamp filename
3. `GET /screenshots` returns JSON list of all stored screenshots
4. All API interactions logged to `app/logs/app.log`
5. Invalid uploads return 400 with descriptive error message
6. Project organized into `app/`, `extension/`, `dashboard/`, `deployment/` folders

**Status:** Not started

---

### Phase 2: Dashboard UI + S3 Cloud Storage
**Goal:** Build a polished web dashboard for viewing screenshots and integrate AWS S3 for cloud backup.

**Requirements:** DB-01, DB-02, DB-03, CS-01, CS-02
**Depends on:** Phase 1

**Success Criteria:**
1. Dashboard displays screenshots in responsive grid layout
2. Each screenshot card shows filename and capture timestamp
3. Dashboard auto-refreshes every 30 seconds without user action
4. Screenshots are uploaded to S3 bucket on capture
5. S3 credentials read from environment variables

**Status:** Not startedl

---

### Phase 3: Chrome Extension
**Goal:** Build a Chrome Extension (Manifest V3) that captures screenshots manually and automatically, sending them to the Flask backend.

**Requirements:** EX-01, EX-02, EX-03, EX-04
**Depends on:** Phase 1

**Success Criteria:**
1. Extension loads in Chrome with proper manifest V3 structure
2. Manual button captures visible tab as PNG screenshot
3. Auto-capture mode takes screenshot every 30 seconds (toggleable)
4. Screenshots are sent to Flask `/upload` endpoint via fetch

**Status:** Not started

---

### Phase 4: DevOps — Docker, Jenkins, Kubernetes
**Goal:** Containerize the application and set up CI/CD pipeline with Kubernetes deployment.

**Requirements:** DP-01, DP-02, DP-03
**Depends on:** Phase 1, Phase 2

**Success Criteria:**
1. `docker build` succeeds and produces working container
2. `docker run` starts Flask app accessible on mapped port
3. Jenkinsfile defines clone → install → build → run pipeline
4. Kubernetes deployment.yaml creates 2 replicas with proper health checks

**Status:** Not started
