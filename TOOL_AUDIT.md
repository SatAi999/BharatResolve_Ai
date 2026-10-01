# BharatResolve AI — Tool Audit & Integration Registry

**Date:** 2026-10-01  
**Module:** `backend/app/tools/registry.py` & `backend/app/tools/`

---

## 1. Overview of Tool Architecture

BharatResolve AI implements a strict Tool Registry where every tool:
1. Defines explicit input parameter schemas.
2. Performs validation prior to execution.
3. Attempts live API calls when keys/endpoints are reachable.
4. Gracefully degrades to verified offline deterministic heuristics if live third-party services fail or return non-200.
5. Returns structured json results with `provenance` metadata.

---

## 2. Integrated Tool Registry

| Tool Name | Target Domain | Real Integration API / Provider | Offline Graceful Fallback Strategy | Risk Level |
| :--- | :--- | :--- | :--- | :---: |
| `fetch_land_records` | Land / Property | Revenue Dept / Bhulekh / Land DB | Verified Mock DB record lookup by Survey No. | Low |
| `fetch_weather_data` | Weather / Agriculture | Open-Meteo REST API (Open) / OpenWeatherMap | Historical climate baseline dataset | Low |
| `fetch_geocoding` | Location / Civic | OpenStreetMap Nominatim API | District coordinate centroid lookup | Low |
| `check_consumer_forum` | Consumer Disputes | NCH / Consumer Commission API | Precedent index search | Medium |
| `check_electricity_status` | Utilities / Power | State Discom Outage Board API | Grid feeder status simulation | Medium |
| `check_water_board_status` | Utilities / Water | Jal Board Metering API | Municipal pressure zone data | Medium |
| `verify_document_ocr` | Legal / Documentation | Tesseract OCR / Gemini Vision | Metadata extraction engine | Low |
| `submit_official_grievance` | Resolution Action | CPGRAMS / Public Grievance Portal API | Simulated queue token generation | **High** |
| `process_utility_refund` | Resolution Action | Discom Billing API / Bank Portal | High-risk gate check requiring human approval | **Critical** |

---

## 3. Real Integration Verification Results

### Open-Meteo Weather API
- **Endpoint:** `https://api.open-meteo.com/v1/forecast`
- **Verification:** Verified live HTTP calls for coordinate lat/long weather retrieval during agricultural damage investigation.
- **Status:** **PASS** (Live REST API functional).

### OpenStreetMap Nominatim Geocoding API
- **Endpoint:** `https://nominatim.openstreetmap.org/search`
- **Verification:** Verified real address-to-coordinate lookup during civic issue intake.
- **Status:** **PASS** (Live REST API functional).

### CPGRAMS / Public Grievance Submission Tool
- **Verification:** Implements mandatory Human-in-the-Loop Risk Gate (`HIGH` risk). Requires user approval signature before dispatching grievance ticket.
- **Status:** **PASS** (Risk policy enforced).
