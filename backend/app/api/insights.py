from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.db import Case, Action, Approval, ToolCall, VerificationResult

router = APIRouter(prefix="/api/insights", tags=["Insights"])

@router.get("")
def get_system_insights(db: Session = Depends(get_db)):
    total_cases = db.query(func.count(Case.id)).scalar() or 0
    if total_cases == 0:
        return {
            "total_cases": 0,
            "status": "Insufficient data",
            "message": "No cases recorded in database yet. Create your first case to see live operational insights.",
            "domain_breakdown": {},
            "avg_resolution_score": 0.0,
            "pending_approvals_count": 0,
            "tool_calls_count": 0,
            "tool_success_rate": 1.0
        }

    # Domain breakdown
    domain_counts = db.query(Case.domain, func.count(Case.id)).group_by(Case.domain).all()
    domain_breakdown = {d[0] or "General Citizen": d[1] for d in domain_counts}

    # Average resolution score
    avg_score = db.query(func.avg(Case.resolution_score)).scalar() or 0.0

    # Approvals & Tool calls count
    pending_approvals = db.query(func.count(Approval.id)).filter(Approval.status == "PENDING").scalar() or 0
    total_tool_calls = db.query(func.count(ToolCall.id)).scalar() or 0
    successful_tool_calls = db.query(func.count(ToolCall.id)).filter(ToolCall.status == "SUCCESS").scalar() or 0
    tool_success_rate = round(successful_tool_calls / max(1, total_tool_calls), 2)

    return {
        "total_cases": total_cases,
        "status": "Active Data Available",
        "domain_breakdown": domain_breakdown,
        "avg_resolution_score": round(float(avg_score), 2),
        "pending_approvals_count": pending_approvals,
        "tool_calls_count": total_tool_calls,
        "tool_success_rate": tool_success_rate
    }
