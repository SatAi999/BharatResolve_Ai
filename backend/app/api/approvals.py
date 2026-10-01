from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.db import Approval, Action, Case
from app.schemas.case_schemas import ApprovalSchema, ApprovalDecision
from app.engine.state_graph import orchestrator

router = APIRouter(prefix="/api/approvals", tags=["Approvals"])

@router.get("", response_model=List[ApprovalSchema])
def list_pending_approvals(db: Session = Depends(get_db)):
    approvals = db.query(Approval).filter(Approval.status == "PENDING").all()
    return [
        ApprovalSchema(
            id=a.id,
            case_id=a.case_id,
            action_id=a.action_id,
            title=a.title,
            reason=a.reason,
            risk_level=a.risk_level,
            status=a.status,
            approved_by=a.approved_by,
            decision_notes=a.decision_notes,
            requested_at=a.requested_at
        ) for a in approvals
    ]

@router.post("/{approval_id}/decide")
async def decide_approval(
    approval_id: str,
    payload: ApprovalDecision,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found")

    approval.status = payload.decision
    approval.approved_by = payload.approved_by
    approval.decision_notes = payload.notes
    approval.decided_at = datetime.utcnow()

    if approval.action_id:
        action = db.query(Action).filter(Action.id == approval.action_id).first()
        if action:
            action.status = "APPROVED" if payload.decision == "APPROVED" else "REJECTED"

    case = db.query(Case).filter(Case.id == approval.case_id).first()
    if case and payload.decision == "APPROVED":
        case.status = "EXECUTING"
        db.commit()

        # Resume agent workflow in background
        background_tasks.add_task(orchestrator.execute_case_workflow, case.id)
    else:
        if case:
            case.status = "REJECTED"
        db.commit()

    return {
        "approval_id": approval.id,
        "case_id": approval.case_id,
        "status": approval.status,
        "decided_at": approval.decided_at
    }
