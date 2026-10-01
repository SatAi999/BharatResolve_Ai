# BharatResolve AI — Known Limitations & System Boundaries

**Document Status:** Production Transparency Specification  
**Version:** 1.0.0

---

## 1. Integrations & Real-World Boundaries

1. **State Discom Direct API Access:**
   - Public Discom portals in certain Indian states require CAPTCHA or OTP authentication. BharatResolve AI operates via official APIs or discom outage feeds. When discom APIs require human OTP verification, the agent halts execution at `PENDING_APPROVAL` and requests OTP input from the user.

2. **Multilingual Speech Processing:**
   - Audio input transcription supports English, Hindi, and Hinglish. Dialects with specific regional variations (e.g. regional Bhojpuri or Marwari colloquialisms) default to Gemini API transcription engines.

3. **CPGRAMS Official Submissions:**
   - Direct automated submission to CPGRAMS requires valid citizen Aadhaar/E-district authentication credentials. BharatResolve AI prepares structured, compliant grievance drafts and mandates human approval before submission.

---

## 2. Technical Operational Constraints

1. **SQLite Concurrent Writes:**
   - In standard single-instance deployment, SQLite manages high read throughput efficiently. For multi-node distributed deployments, SQLite should be swapped for PostgreSQL by updating `DATABASE_URL`.

2. **File Size Limits:**
   - Multimodal document OCR uploads are currently limited to 15MB per PDF/image file to ensure low-latency processing.
