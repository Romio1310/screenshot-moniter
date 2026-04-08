# Requirements — Intelligent Screenshot Monitoring System

## v1 Requirements

### Backend Core (BE)
- [ ] **BE-01**: Flask app with structured project layout and logging enabled — Phase 1
- [ ] **BE-02**: GET `/` returns system status JSON — Phase 1
- [ ] **BE-03**: POST `/upload` accepts screenshot via multipart form — Phase 1
- [ ] **BE-04**: GET `/screenshots` returns list of all stored screenshots — Phase 1
- [ ] **BE-05**: All uploads, errors, and API hits logged to file — Phase 1

### Screenshot Storage (SS)
- [ ] **SS-01**: Screenshots saved to local folder with timestamp-based filenames — Phase 1
- [ ] **SS-02**: Invalid uploads (wrong format, missing file) return proper error responses — Phase 1
- [ ] **SS-03**: Missing file/directory errors handled gracefully — Phase 1

### Dashboard (DB)
- [ ] **DB-01**: Web dashboard displays screenshots in responsive grid layout — Phase 2
- [ ] **DB-02**: Each screenshot shows capture timestamp — Phase 2
- [ ] **DB-03**: Dashboard auto-refreshes every 30 seconds — Phase 2

### Cloud Storage (CS)
- [ ] **CS-01**: Screenshots uploaded to AWS S3 using boto3 — Phase 2
- [ ] **CS-02**: S3 credentials configurable via environment variables (placeholder) — Phase 2

### Chrome Extension (EX)
- [ ] **EX-01**: Chrome Extension with Manifest V3 structure — Phase 3
- [ ] **EX-02**: Manual screenshot button captures current tab — Phase 3
- [ ] **EX-03**: Auto-capture screenshot every 30 seconds (toggleable) — Phase 3
- [ ] **EX-04**: Captured screenshots sent to Flask backend via fetch API — Phase 3

### Deployment (DP)
- [ ] **DP-01**: Dockerfile for Flask backend — Phase 4
- [ ] **DP-02**: Jenkinsfile with clone, install, build, run stages — Phase 4
- [ ] **DP-03**: Kubernetes deployment.yaml with 2 replicas — Phase 4
- [ ] **DP-04**: Project organized into app/, extension/, dashboard/, deployment/ folders — Phase 1

## v2 Requirements (Deferred)

- User authentication and access control
- Screenshot OCR and content analysis
- WebSocket-based real-time dashboard updates
- Multi-tenant workspace support
- Screenshot comparison and diff detection

## Out of Scope

- Database integration — File-based storage is sufficient for v1
- Real-time streaming — Polling-based refresh is adequate
- Mobile app — Chrome extension only for v1

## Traceability

| Phase | Requirements |
|-------|-------------|
| Phase 1 | BE-01, BE-02, BE-03, BE-04, BE-05, SS-01, SS-02, SS-03, DP-04 |
| Phase 2 | DB-01, DB-02, DB-03, CS-01, CS-02 |
| Phase 3 | EX-01, EX-02, EX-03, EX-04 |
| Phase 4 | DP-01, DP-02, DP-03 |
