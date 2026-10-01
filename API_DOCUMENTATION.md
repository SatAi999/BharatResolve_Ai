# BharatResolve AI — REST API Reference Documentation

**Base URL:** `http://localhost:8000/api`  
**Protocol:** HTTP/1.1 REST + SSE (Server-Sent Events)

---

## 1. Case Management Endpoints

### `POST /api/cases`
Creates a new case from raw user problem text, audio transcription, or Hinglish input.
- **Request Body:**
  ```json
  {
    "description": "My electricity bill for consumer account 1048576 is double the normal rate.",
    "user_id": "user_123",
    "language": "en"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "case_id": "case_550e8400",
    "status": "INVESTIGATING",
    "category": "UTILITIES",
    "current_node": "investigate",
    "timeline": [...]
  }
  ```

### `GET /api/cases/{case_id}`
Retrieves complete case details, full timeline, evidence items, resolution score, and current graph state.

### `GET /api/cases/{case_id}/stream`
Server-Sent Events (SSE) streaming endpoint delivering real-time state updates, tool output logs, and reasoning trace tokens to the frontend UI.

---

## 2. Document & Multimodal OCR Endpoints

### `POST /api/documents/upload`
Uploads a document (PDF, PNG, JPG) associated with a case ID.
- **Multipart Form Data:** `file`, `case_id`
- **Response (200 OK):**
  ```json
  {
    "document_id": "doc_8849",
    "extracted_text": "CONSUMER NO: 1048576 AMOUNT DUE: RS 14,200...",
    "metadata": {
      "consumer_no": "1048576",
      "amount": 14200.0
    }
  }
  ```

---

## 3. Approval Workbench Endpoints

### `GET /api/approvals/pending`
Lists all cases currently blocked at node `pending_approval` waiting for human authorization.

### `POST /api/cases/{case_id}/approve`
Submits approval or rejection decision for a pending high-risk action.
- **Request Body:**
  ```json
  {
    "approval_id": "app_9912",
    "approved": true,
    "decision_notes": "Verified billing anomaly on discom portal."
  }
  ```
- **Response (200 OK):** Resumes graph execution at node `execute_action`.

---

## 4. Counterfactual Analysis Endpoint

### `POST /api/counterfactual/analyze`
Executes counterfactual simulation on a case.
- **Request Body:**
  ```json
  {
    "case_id": "case_550e8400",
    "modified_inputs": {"bill_receipt_uploaded": true}
  }
  ```
- **Response (200 OK):** Returns predicted resolution score delta and confidence change.

---

## 5. Health & Integration Probes

### `GET /health`
Returns system status, active database connections, vector DB status, and LLM provider connectivity.
