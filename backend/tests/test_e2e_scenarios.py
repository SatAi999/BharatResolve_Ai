import pytest
import asyncio
from app.db.session import SessionLocal, Base, engine
from app.models.db import Case, Action, Approval, Document, Evidence
from app.engine.state_graph import orchestrator

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

@pytest.mark.asyncio
async def test_case_1_scholarship_investigation():
    with SessionLocal() as db:
        c = Case(
            title="NSP Scholarship Payment Case",
            raw_input="My NSP scholarship of Rs 12000 was approved 2 months ago but payment not received in bank account",
            domain="Education",
            intent="Scholarship Support"
        )
        db.add(c)
        db.commit()
        case_id = c.id

    state = await orchestrator.execute_case_workflow(case_id)
    assert state.case_id == case_id
    assert any(d in state.domain for d in ["Education", "General Citizen", "Financial Services", "GovTech"])

@pytest.mark.asyncio
async def test_case_2_electricity_bill_anomaly():
    with SessionLocal() as db:
        c = Case(
            title="Electricity Bill Anomaly Case",
            raw_input="My electricity bill for June jumped from Rs 1200 to Rs 18400. Meter number meter-889977 in Jaipur Rajasthan",
            domain="Utilities",
            intent="Bill Anomaly"
        )
        db.add(c)
        db.commit()
        case_id = c.id

    state = await orchestrator.execute_case_workflow(case_id)
    assert state.case_id == case_id
    assert len(state.evidence_items) > 0

@pytest.mark.asyncio
async def test_case_3_agriculture_weather_check():
    with SessionLocal() as db:
        c = Case(
            title="PM Fasal Bima Crop Damage Case",
            raw_input="Heavy unseasonal rain damaged my wheat crop in Varanasi Uttar Pradesh. How to claim PM Fasal Bima Yojana relief?",
            domain="Agriculture",
            intent="Crop Damage Relief"
        )
        db.add(c)
        db.commit()
        case_id = c.id

    state = await orchestrator.execute_case_workflow(case_id)
    assert state.case_id == case_id
    assert any("Open-Meteo" in ev.get("source_title", "") for ev in state.evidence_items)

@pytest.mark.asyncio
async def test_case_4_approval_pause_and_rejection():
    with SessionLocal() as db:
        c = Case(
            title="Municipal Water Grievance Case",
            raw_input="File a formal complaint against municipal water supply department",
            domain="Citizen/GovTech",
            intent="Grievance Preparation"
        )
        db.add(c)
        db.commit()
        case_id = c.id

    # 1. State graph should pause at approval_wait
    state = await orchestrator.execute_case_workflow(case_id)
    assert state.status == "PENDING_APPROVAL"
    assert state.is_paused_for_approval is True

    # 2. Simulate User Rejection
    with SessionLocal() as db:
        ap = db.query(Approval).filter(Approval.case_id == case_id).first()
        assert ap is not None
        ap.status = "REJECTED"
        case_obj = db.query(Case).filter(Case.id == case_id).first()
        case_obj.status = "REJECTED"
        db.commit()

    with SessionLocal() as db:
        c_check = db.query(Case).filter(Case.id == case_id).first()
        assert c_check.status == "REJECTED"
