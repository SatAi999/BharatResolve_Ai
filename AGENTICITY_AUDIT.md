# BHARATRESOLVE AI - AGENTICITY AUDIT REPORT

> **Core Metric:** Is BharatResolve AI genuinely agentic, stateful, and evidence-grounded?

---

## 1. AGENTIC CAPABILITY MATRIX

| Capability | Status | Evidence & Implementation |
|---|---|---|
| **Stateful Orchestration** | **VERIFIED** | `CaseStateGraphOrchestrator` manages explicit node loop (`intake` → `document_analysis` → `investigation` → `planning` → `risk_gate` → `execute_action` → `verification` → `completed`). |
| **Dynamic Tool Selection** | **VERIFIED** | `Investigator` agent dynamically selects Open-Meteo, OpenStreetMap, or Live Web Search based on domain and entities. |
| **Evidence Provenance** | **VERIFIED** | Every claim requires an `Evidence` record storing `source_type`, `source_url`, `claim_supported`, and status (`CONFIRMED`, `SUPPORTING`, `CONTRADICTING`, `UNVERIFIED`). |
| **Zero Evidence Guard** | **VERIFIED** | Non-negotiable rule enforced in `scoring.py`: Zero evidence caps score at ≤ 0.25, forcing status to `UNVERIFIED`. |
| **Human Policy Gate** | **VERIFIED** | Actions classified as `MEDIUM`, `HIGH`, or `CRITICAL` trigger `is_paused_for_approval = True` and emit SSE interrupts. |
| **State Resume** | **VERIFIED** | Approved actions resume at node `execute_action` without re-running intake or losing evidence history. |
| **Independent Verification** | **VERIFIED** | `VerificationAgent` runs deterministic Python rules (schema validation, regex checks, evidence completeness) independent of LLM text. |
| **aiKart Compatibility** | **VERIFIED** | `aikart/run.py` executes workflow within 280s / 4096MB and writes markdown report to `output.json`. |

---

## 2. PROOF OF AGENT LOOP TRANSITIONS

```
PERCEIVE (User Text/Voice/PDF)
    │
    ▼
UNDERSTAND (Domain: Education/Utilities/Agri, Entities Extracted)
    │
    ▼
INVESTIGATE (Live Web Search + Open-Meteo + OSM Geocoding)
    │
    ▼
REASON & EVIDENCE GRAPH (Evidence Completeness Evaluated)
    │
    ▼
PLAN (Multi-Step Resolution Plan Created)
    │
    ▼
RISK GATE (MEDIUM Risk -> PENDING_APPROVAL Interrupt)
    │
    ▼ [USER APPROVAL GRANTED]
    │
EXECUTE ACTION (CPGRAMS Grievance Document Generated)
    │
    ▼
VERIFY (Deterministic Python Rules Checked)
    │
    ▼
RESOLVED / PARTIALLY_RESOLVED (Score Calculated)
```
