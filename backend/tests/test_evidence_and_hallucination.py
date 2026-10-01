import pytest
from app.schemas.case_schemas import EvidenceSchema
from app.engine.evidence_engine import evaluate_evidence_graph
from app.engine.scoring import calculate_resolution_score

def test_zero_evidence_evaluation():
    result = evaluate_evidence_graph([])
    assert result["completeness_score"] == 0.0
    assert result["status"] == "UNVERIFIED"
    assert result["has_contradictions"] is False

def test_contradicting_evidence_evaluation():
    evidence_list = [
        EvidenceSchema(source_type="web_research", source_title="Official Source A", claim_supported="Status Approved", status="CONFIRMED"),
        EvidenceSchema(source_type="user_input", source_title="Citizen Note", claim_supported="Status Cancelled", status="CONTRADICTING")
    ]
    result = evaluate_evidence_graph(evidence_list)
    assert result["has_contradictions"] is True
    assert result["status"] == "CONTRADICTED"

def test_resolution_score_zero_evidence_guard():
    """
    Ensures zero evidence strictly caps or zero-weights resolution score
    so an unevidenced claim can never falsely report RESOLVED.
    """
    # 0 evidence completeness
    score = calculate_resolution_score(
        evidence_completeness=0.0,
        action_completed=True,
        verification_passed=True,
        unresolved_dependencies_count=0,
        confidence_score=0.85
    )
    # Score with 0 evidence must not cross 0.50 threshold for resolution
    assert score <= 0.50, f"Expected score <= 0.50 for zero evidence, got {score}"
