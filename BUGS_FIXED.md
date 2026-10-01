# BHARATRESOLVE AI - BUGS FOUND & FIXED FORENSIC LOG

---

## 1. DEFECT DISCOVERY & RESOLUTION MATRIX

### DEFECT P0-01: Zero-Evidence Hallucination Vulnerability
- **Severity:** P0 — Critical Security & Truthfulness Violation
- **Affected Component:** `backend/app/engine/scoring.py` & `state_graph.py`
- **Root Cause:** `calculate_resolution_score` evaluated action completion, verification, and confidence score without requiring `evidence_completeness > 0.0`. A case with zero evidence items received a score of `0.67` (> 0.60 threshold), allowing unevidenced cases to falsely reach `RESOLVED` status.
- **Expected Behavior:** Non-Negotiable Rule 18: NO EVIDENCE = NO DEFINITIVE CLAIM. Zero evidence must hard-cap the score at ≤ 0.25 and force status to `UNVERIFIED`.
- **Actual Behavior:** uneventfully returned score 0.67 and marked case `RESOLVED`.
- **Fix Applied:** Modified `scoring.py` and `state_graph.py` to check `if evidence_completeness == 0.0: return 0.25 if action_completed else 0.0`. Added hard zero-evidence check forcing `UNVERIFIED` status in `run_verification_stage`.
- **Regression Test:** `test_evidence_and_hallucination.py::test_resolution_score_zero_evidence_guard` (PASS).

---

### DEFECT P1-02: State Persistence & Resume Entry Node Bug
- **Severity:** P1 — Critical State Machine Defect
- **Affected Component:** `backend/app/engine/state_graph.py` (`execute_case_workflow`)
- **Root Cause:** When loading a case paused for approval (`PENDING_APPROVAL`), `state.current_node` defaulted to `"intake"`. Resuming an approved case re-executed intake from scratch instead of entering node `"execute_action"`.
- **Expected Behavior:** Paused case resumes directly at node `"execute_action"` upon approval without losing evidence or restarting intake.
- **Actual Behavior:** Workflow restarted at intake, re-extracting intent and duplicating database entities.
- **Fix Applied:** Refactored `execute_case_workflow` in `state_graph.py` to inspect persisted case and action status to set initial `current_node = "execute_action"` if status is `PENDING_APPROVAL` or `EXECUTING`. Reconstructed existing evidence, entities, and actions into `AgentState`.
- **Regression Test:** `test_agent_state_graph.py::test_case_resume_after_approval` (PASS).

---

### DEFECT P1-03: Null Title Database Constraint Failure
- **Severity:** P1 — Database Integrity Failure
- **Affected Component:** `backend/app/models/db.py` (`Case.title`)
- **Root Cause:** Column `Case.title` had `nullable=False` without a default value, causing `sqlite3.IntegrityError` when instantiated without an explicit title keyword argument.
- **Expected Behavior:** `Case(raw_input=...)` automatically defaults `title` to `"Citizen Grievance Case"` or raw input preview.
- **Actual Behavior:** SQLite raise NOT NULL constraint error during transaction flush.
- **Fix Applied:** Updated `Case.title` in `models/db.py` to `default="Citizen Grievance Case"`.
- **Regression Test:** `test_e2e_scenarios.py::test_case_1_scholarship_investigation` (PASS).
