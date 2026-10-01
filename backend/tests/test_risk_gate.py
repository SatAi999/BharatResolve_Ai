import pytest
from app.engine.risk_gate import evaluate_action_risk

def test_risk_classification():
    level, requires_approval, reason = evaluate_action_risk("prepare_grievance", {})
    assert level == "MEDIUM"
    assert requires_approval is True

    level_low, req_low, _ = evaluate_action_risk("search_official_information", {})
    assert level_low == "LOW"
    assert req_low is False

    level_crit, req_crit, _ = evaluate_action_risk("financial_disbursement", {})
    assert level_crit == "CRITICAL"
    assert req_crit is True
