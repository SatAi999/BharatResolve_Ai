import pytest
from app.engine.scoring import calculate_resolution_score, run_counterfactual_precheck

def test_resolution_score_formula():
    score = calculate_resolution_score(
        evidence_completeness=1.0,
        action_completed=True,
        verification_passed=True,
        unresolved_dependencies_count=0,
        confidence_score=0.9
    )
    assert score == 0.99

def test_counterfactual_precheck():
    result = run_counterfactual_precheck(
        raw_input="Scholarship issue",
        extracted_fields={},
        documents_count=0
    )
    assert result.status in ["WARNING", "BLOCKED"]
    assert len(result.missing_fields) > 0
    assert len(result.recommendations) > 0
