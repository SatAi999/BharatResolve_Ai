import json
import asyncio
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.db import (
    Case, CaseMessage, CaseEntity, Document, Evidence, Hypothesis, Plan, Action, Approval, VerificationResult, AuditEvent
)
from app.schemas.case_schemas import CaseCreate, CaseResponse, EntitySchema, EvidenceSchema, HypothesisSchema, PlanSchema, ActionSchema, ApprovalSchema, VerificationResultSchema, AuditEventSchema
from app.engine.state_graph import orchestrator

router = APIRouter(prefix="/api/cases", tags=["Cases"])

def format_case_response(case: Case, db: Session) -> CaseResponse:
    entities = [EntitySchema(entity_type=e.entity_type, entity_value=e.entity_value, confidence=e.confidence, source=e.source) for e in case.entities]
    evidence_items = [EvidenceSchema(id=e.id, source_type=e.source_type, source_title=e.source_title, source_url=e.source_url, claim_supported=e.claim_supported, confidence=e.confidence, status=e.status, retrieved_at=e.retrieved_at) for e in case.evidence_items]
    hypotheses = [HypothesisSchema(id=h.id, description=h.description, status=h.status, confidence=h.confidence, supporting_evidence_ids=h.supporting_evidence_ids or []) for h in case.hypotheses]
    
    plans = []
    for p in case.plans:
        steps = [{"id": s.id, "step_number": s.step_number, "title": s.title, "description": s.description, "action_type": s.action_type, "risk_level": s.risk_level, "status": s.status, "result_summary": s.result_summary} for s in p.steps]
        plans.append(PlanSchema(id=p.id, objective=p.objective, status=p.status, steps=steps))

    actions = [ActionSchema(id=a.id, action_name=a.action_name, description=a.description, risk_level=a.risk_level, requires_approval=a.requires_approval, status=a.status, payload=a.payload, output_result=a.output_result) for a in case.actions]
    approvals = [ApprovalSchema(id=ap.id, case_id=ap.case_id, action_id=ap.action_id, title=ap.title, reason=ap.reason, risk_level=ap.risk_level, status=ap.status, approved_by=ap.approved_by, decision_notes=ap.decision_notes, requested_at=ap.requested_at) for ap in case.approvals]
    verification_results = [VerificationResultSchema(id=v.id, verification_type=v.verification_type, status=v.status, details=v.details, verified_at=v.verified_at) for v in case.verification_results]
    audit_events = [AuditEventSchema(id=au.id, event_type=au.event_type, actor=au.actor, payload=au.payload, created_at=au.created_at) for au in case.audit_events]

    messages = [{"id": m.id, "sender": m.sender, "content": m.content, "message_type": m.message_type, "created_at": m.created_at.isoformat()} for m in case.messages]

    return CaseResponse(
        id=case.id,
        title=case.title,
        raw_input=case.raw_input,
        normalized_problem=case.normalized_problem,
        domain=case.domain or "General Citizen",
        intent=case.intent or "Investigation",
        language=case.language or "en",
        urgency=case.urgency or "MEDIUM",
        status=case.status,
        risk_level=case.risk_level or "LOW",
        confidence_score=case.confidence_score or 0.0,
        resolution_score=case.resolution_score or 0.0,
        summary=case.summary,
        created_at=case.created_at,
        updated_at=case.updated_at,
        messages=messages,
        entities=entities,
        evidence_items=evidence_items,
        hypotheses=hypotheses,
        plans=plans,
        actions=actions,
        approvals=approvals,
        verification_results=verification_results,
        audit_events=audit_events
    )

@router.post("", response_model=CaseResponse)
async def create_case(payload: CaseCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    case = Case(
        title=payload.raw_input[:60] + "...",
        raw_input=payload.raw_input,
        language=payload.language,
        status="CREATED"
    )
    db.add(case)
    db.commit()
    db.refresh(case)

    # Initial user message
    msg = CaseMessage(
        case_id=case.id,
        sender="user",
        content=payload.raw_input,
        message_type="voice_transcript" if payload.voice_file_path else "text"
    )
    db.add(msg)
    db.commit()

    # Trigger agent workflow in background
    background_tasks.add_task(orchestrator.execute_case_workflow, case.id)

    return format_case_response(case, db)

@router.get("", response_model=List[CaseResponse])
def list_cases(domain: Optional[str] = None, status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Case)
    if domain:
        query = query.filter(Case.domain == domain)
    if status:
        query = query.filter(Case.status == status)
    cases = query.order_by(Case.created_at.desc()).all()
    return [format_case_response(c, db) for c in cases]

@router.get("/{case_id}", response_model=CaseResponse)
def get_case(case_id: str, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
    return format_case_response(case, db)

@router.get("/{case_id}/stream")
async def stream_case_events(case_id: str, db: Session = Depends(get_db)):
    """Server-Sent Events (SSE) endpoint providing real-time operational agent events."""
    async def event_generator():
        last_event_count = 0
        while True:
            case = db.query(Case).filter(Case.id == case_id).first()
            if not case:
                yield f"data: {json.dumps({'event': 'error', 'message': 'Case not found'})}\n\n"
                break

            events = case.audit_events
            if len(events) > last_event_count:
                for ev in events[last_event_count:]:
                    payload = {
                        "event_type": ev.event_type,
                        "actor": ev.actor,
                        "payload": ev.payload,
                        "case_status": case.status,
                        "timestamp": ev.created_at.isoformat()
                    }
                    yield f"data: {json.dumps(payload)}\n\n"
                last_event_count = len(events)

            if case.status in ["RESOLVED", "PARTIALLY_RESOLVED", "UNVERIFIED", "FAILED", "PENDING_APPROVAL"]:
                final_payload = {
                    "event_type": "StateUpdate",
                    "case_status": case.status,
                    "resolution_score": case.resolution_score,
                    "summary": case.summary
                }
                yield f"data: {json.dumps(final_payload)}\n\n"
                break

            await asyncio.sleep(1.0)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
