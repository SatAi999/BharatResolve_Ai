# BharatResolve AI — Release Changelog

All notable changes to the BharatResolve AI codebase are documented in this file.

---

## [1.0.0] - 2026-10-01 (Final Release Hardening & Production Candidate)

### Added
- **Final Documentation Suite:** Added `FINAL_TEST_MATRIX.md`, `STATE_TRANSITION_AUDIT.md`, `TOOL_AUDIT.md`, `ARCHITECTURE.md`, `API_DOCUMENTATION.md`, `FAILURE_INJECTION_REPORT.md`, `DEPLOYMENT.md`, `KNOWN_LIMITATIONS.md`, `CHANGELOG.md`.
- **Deployment Configurations:** Added `render.yaml` for Render backend web service and `vercel.json` for Vercel Next.js frontend deployment.
- **Configurable CORS:** Updated `config.py` and `main.py` to parse comma-separated `ALLOWED_ORIGINS` environment variables for production security.
- **Full Test Suite:** 16 automated pytest suites validating all agent state graph transitions, evidence scoring, risk gating, OCR document intake, approvals, counterfactual engine, and REST APIs.

### Fixed
- **[P0] Anti-Hallucination Guard (`backend/app/services/scoring.py`):** Fixed critical vulnerability where cases with `evidence_completeness == 0.0` could reach status `RESOLVED`. Forced resolution score cap to `<= 0.25` and status `UNVERIFIED`.
- **[P1] Approval Resume Node (`backend/app/agent/state_graph.py`):** Fixed state resume bug where approving a pending high-risk action reset graph execution to `intake` node instead of directly executing action node (`execute_action`).
- **[P1] Null Case Title Safeguard (`backend/app/models/db.py`):** Fixed database schema non-null title constraint error by adding fallback title auto-generation during initial case intake.

### Hardened
- **Verification Integrity:** Audited all 9 tools in `backend/app/tools/registry.py` ensuring zero hardcoded or fabricated responses. Real live REST calls (Open-Meteo, OSM Nominatim) verified.
- **Next.js Frontend Build:** Verified production static page compilation (`npm run build`, 10/10 routes passing).
- **aiKart Evaluation Runner:** Executed `aikart/run.py` to generate complete evaluation run trace output.
