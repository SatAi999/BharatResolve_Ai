import pytest
import asyncio
from app.db.session import SessionLocal, Base, engine
from app.models.db import Case, Action, Approval, Evidence, AuditEvent
from app.engine.state_graph import orchestrator

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

@pytest.mark.asyncio
async def test_case_resume_after_approval():
    """
    Test that when a case is paused for approval and then approved,
    the state graph resumes at 'execute_action' rather than restarting at 'intake'.
    """
    with SessionLocal() as db:
        c = Case(
            title="Scholarship Grievance Case",
            raw_input="Need payment disbursement for approved NSP scholarship",
            domain="Education",
            intent="Scholarship Support",
            status="PENDING_APPROVAL",
            risk_level="MEDIUM"
        )
        db.add(c)
        db.commit()
        db.refresh(c)

        # Add evidence item
        ev = Evidence(
            case_id=c.id,
            source_type="web_research",
            source_title="NSP Grievance Portal Guidelines",
            claim_supported="DBT disbursement pending nodal officer verification",
            status="CONFIRMED"
        )
        db.add(ev)

        # Add prepared action and pending approval with full valid schema payload
        action = Action(
            case_id=c.id,
            action_name="prepare_grievance",
            description="Generate official representation",
            risk_level="MEDIUM",
            requires_approval=True,
            status="APPROVED",
            payload={
                "grievance_type": "CPGRAMS",
                "applicant_name": "Test Citizen",
                "target_authority": "NSP Nodal Office",
                "case_summary": "Scholarship approved but DBT payment missing",
                "desired_relief": "Expedited disbursement to bank account"
            }
        )
        db.add(action)
        db.commit()
        case_id = c.id

    # Execute workflow on approved case
    final_state = await orchestrator.execute_case_workflow(case_id)
    
    # State should reach completed and executed action
    assert final_state.current_node == "completed"
    assert len(final_state.actions) > 0
    assert final_state.actions[0]["status"] == "EXECUTED"

    with SessionLocal() as db:
        updated_case = db.query(Case).filter(Case.id == case_id).first()
        assert updated_case.status in ["RESOLVED", "PARTIALLY_RESOLVED", "UNVERIFIED"]
