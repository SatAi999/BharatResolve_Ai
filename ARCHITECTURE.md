# BharatResolve AI — Technical Architecture Specification

**Version:** 1.0.0  
**Stack:** FastAPI (Python 3.10) + Next.js 14 (TypeScript, Tailwind CSS) + LangGraph + SQLite/Qdrant

---

## 1. System Topology Overview

```
 ┌─────────────────────────────────────────────────────────┐
 │                   Next.js 14 Frontend                   │
 │ (Chat UI, Case Graph Visualization, Evidence Drawer,   │
 │  Approval Workbench, Counterfactual Analysis Panel)      │
 └────────────────────────────┬────────────────────────────┘
                              │ REST APIs + Realtime SSE Stream
 ┌────────────────────────────▼────────────────────────────┐
 │                  FastAPI Application Server             │
 ├─────────────────────────────────────────────────────────┤
 │ 1. Intake Parser (Multimodal Text/Audio/OCR)            │
 │ 2. LangGraph Agent Case Engine (State Graph Nodes)      │
 │ 3. Tool Execution Registry (Open-Meteo, OSM, Bhulekh)   │
 │ 4. Risk Gate & Human-in-the-Loop Policy Engine          │
 │ 5. Evidence Engine & Hallucination Guard                │
 │ 6. Scoring & Counterfactual Root Cause Analysis         │
 └──────────────┬──────────────────────────┬───────────────┘
                │                          │
 ┌──────────────▼──────────┐    ┌──────────▼───────────────┐
 │   SQLite DB (Metadata,  │    │  Qdrant / Vector Search  │
 │  Cases, Approvals, SSE) │    │  (Precedents, Statutes)  │
 └─────────────────────────┘    └──────────────────────────┘
```

---

## 2. Core Subsystems

### 2.1 Multimodal Intake Engine (`backend/app/api/documents.py`)
- Accepts raw text, Hinglish, voice transcriptions, images (JPEG/PNG), and PDFs.
- Utilizes OCR fallback engines to extract survey numbers, billing IDs, transaction reference codes, and timestamps.

### 2.2 LangGraph State Engine (`backend/app/agent/state_graph.py`)
- Maintains deterministic state transitions through graph nodes: `intake` -> `investigate` -> `reason_and_score` -> `risk_gate` -> `execute_action` -> `verify_results`.
- Enforces pause/resume capabilities when cases require human intervention.

### 2.3 Evidence & Anti-Hallucination Guard (`backend/app/services/scoring.py`)
- Evaluates evidence provenance for every claim made by the agent.
- Hard caps resolution score to `<= 0.25` and forces status to `UNVERIFIED` if no concrete evidence items support the resolution.

### 2.4 Human-in-the-Loop Risk Gate (`backend/app/services/risk_gate.py`)
- Classifies actions by risk level (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).
- Requires signed approval for high-risk actions (e.g. submitting official grievances or disbursing refunds).

### 2.5 Counterfactual Root Cause Engine (`backend/app/services/counterfactual_engine.py`)
- Generates "what-if" scenarios analyzing how outcome confidence would change if specific evidence items or missing user inputs were provided.

---

## 3. Data Flow Diagram

```
User Input ──► Multimodal Intake ──► Graph State Node ──► Tool Execution Engine
                                                                 │
                                                                 ▼
Resolution Verified ◄── Risk Gate Check ◄── Evidence Engine ◄── Real API / Fallback
```
