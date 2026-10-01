# BharatResolve AI — State Transition Audit Report

**Date:** 2026-10-01  
**System:** LangGraph Case Engine  
**Module:** `backend/app/agent/state_graph.py` & `backend/app/agent/state.py`

---

## 1. Overview of Case Lifecycle States

BharatResolve AI uses a deterministic state graph governing all case progression. States cannot be bypassed, skipped, or manually mutated to `RESOLVED` without satisfying evidence provenance rules.

```
       [INTAKE]
          │
          ▼
   [INVESTIGATE] ◄──── (Missing Data Request)
          │
          ▼
   [REASON & SCORE]
          │
    ┌─────┴────────────────┐
    │ Risk Assessment      │
    ▼                      ▼
[LOW / MED RISK]     [HIGH / CRITICAL RISK]
    │                      │
    ▼                      ▼
[EXECUTE ACTION]   [PENDING APPROVAL]
    │                      │
    │                      ├─────────► (Approved) ────► [EXECUTE ACTION]
    │                      │
    │                      └─────────► (Rejected) ────► [REASON & SCORE]
    ▼
[VERIFY RESULTS]
    │
    ├─────────► (Confidence >= 0.70 & Evidence > 0) ──► [RESOLVED]
    │
    └─────────► (Confidence < 0.70 OR Evidence == 0) ──► [UNVERIFIED / ESCALATED]
```

---

## 2. State Node Audit Matrix

| Node Name | Input State Preconditions | State Mutated | Next State Transition | Safety Check / Gate |
| :--- | :--- | :--- | :--- | :--- |
| `intake` | Unstructured text, audio, image, PDF | Category, domain, urgency, extracted entities | `investigate` | Sanitizes input for prompt injections |
| `investigate` | Case entity structure | Evidence list, tool execution logs | `reason_and_score` | Executes domain tools (Weather, Land Records, Consumer Forum, PSS, Water Board) |
| `reason_and_score` | Gathered evidence items | Hypothesis list, resolution score, confidence | `risk_gate` | Calculates evidence completeness. Hard caps score at 0.25 if evidence count is 0 |
| `risk_gate` | Resolution score, proposed action | Risk level (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), `requires_approval` | `execute_action` OR `pending_approval` | Routes actions mutating official records or initiating refunds to `pending_approval` |
| `pending_approval` | `requires_approval == True` | `approval_id`, decision status | `execute_action` (Approved) OR `reason_and_score` (Rejected) | Blocks agent execution until explicit human authorization API call |
| `execute_action` | Authorized action call | Execution output payload, action result log | `verify_results` | Handles tool failures, records actual tool return codes |
| `verify_results` | Action result log | Case status (`RESOLVED`, `UNVERIFIED`, `ESCALATED`), final audit summary | Terminal State | Validates post-execution evidence state |

---

## 3. Approval & Re-entry Safeguard Verification

When a case enters `PENDING_APPROVAL`:
1. Graph execution pauses and serializes current state to SQLite database `Case` & `Approval` models.
2. User submits approval via `/api/cases/{case_id}/approve`.
3. Resume logic re-hydrates graph state and explicitly sets entry node to `execute_action`.
4. Tests (`tests/test_approvals_api.py` and `tests/test_agent_state_graph.py`) confirm state resumes at `execute_action` rather than looping back to `intake`.

---

## 4. Anti-Hallucination Terminal Rules

- A case **CANNOT** reach status `RESOLVED` if `evidence_completeness == 0.0`.
- Under zero evidence conditions, `verify_results` forces status to `UNVERIFIED` and logs an anti-hallucination warning in the audit trail.
