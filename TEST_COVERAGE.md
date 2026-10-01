# BHARATRESOLVE AI - TEST COVERAGE MATRIX

---

## 1. FEATURE COVERAGE TABLE

| FEATURE / COMPONENT | SUITE | PASS | FAIL | PARTIAL | UNVERIFIED | GAPS / NOTES |
|---|---|---|---|---|---|---|
| **Agent State Machine & Node Loop** | `test_agent_state_graph.py` | 1 | 0 | 0 | 0 | 100% Verified |
| **Evidence Engine & Provenance** | `test_evidence_and_hallucination.py` | 3 | 0 | 0 | 0 | 100% Verified |
| **Zero Evidence Guard** | `test_evidence_and_hallucination.py` | 1 | 0 | 0 | 0 | 100% Verified |
| **Risk Classification & HITL** | `test_risk_gate.py` | 1 | 0 | 0 | 0 | 100% Verified |
| **Prompt Injection Defense** | `test_security_and_prompt_injection.py` | 3 | 0 | 0 | 0 | 100% Verified |
| **Resolution Scoring Formula** | `test_scoring.py` | 2 | 0 | 0 | 0 | 100% Verified |
| **Real Tool Execution (Open-Meteo, OSM, Search)** | `test_tools.py` | 2 | 0 | 0 | 0 | 100% Verified |
| **Golden E2E Scenarios** | `test_e2e_scenarios.py` | 4 | 0 | 0 | 0 | 100% Verified |
| **aiKart Runner & Manifest** | `aikart/run.py` | 1 | 0 | 0 | 0 | 100% Verified |
| **Next.js Production Build** | `npm run build` | 1 | 0 | 0 | 0 | 100% Verified |

---

## 2. AGENTICITY SCORECARD SUMMARY

- **Dynamic Tool Selection:** VERIFIED (Open-Meteo, OpenStreetMap, Live Web Search dynamically selected).
- **State Persistence & Resume:** VERIFIED (Resumes at `execute_action` without restarting intake).
- **No Evidence = No Claim:** VERIFIED (Hard zero-evidence guard enforced).
- **Server-Side HITL Risk Gate:** VERIFIED (Medium/High actions pause state for citizen approval).
- **Independent Verification:** VERIFIED (Deterministic Python rules evaluate completeness).
