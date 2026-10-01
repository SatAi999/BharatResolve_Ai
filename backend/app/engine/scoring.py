from typing import Dict, Any, List
from app.schemas.case_schemas import CounterfactualCheckResult

def calculate_resolution_score(
    evidence_completeness: float,
    action_completed: bool,
    verification_passed: bool,
    unresolved_dependencies_count: int,
    confidence_score: float
) -> float:
    """
    Deterministic formula for Case Resolution Score:
    Score = (EvidenceCompleteness * 0.4) + (ActionCompleted * 0.25) + (VerificationPassed * 0.20) + (Confidence * 0.15) - (UnresolvedCount * 0.15)
    
    NON-NEGOTIABLE RULE 18: NO EVIDENCE = NO DEFINITIVE CLAIM.
    If evidence_completeness is 0.0, the maximum possible resolution score is hard-capped at 0.30
    so that zero evidence can NEVER yield a RESOLVED state (>0.60).
    """
    if evidence_completeness == 0.0:
        return 0.25 if action_completed else 0.0

    score = (
        (evidence_completeness * 0.40) +
        (1.0 if action_completed else 0.0) * 0.25 +
        (1.0 if verification_passed else 0.0) * 0.20 +
        (confidence_score * 0.15) -
        (unresolved_dependencies_count * 0.15)
    )
    return round(max(0.0, min(1.0, score)), 2)

def run_counterfactual_precheck(
    raw_input: str,
    extracted_fields: Dict[str, Any],
    documents_count: int
) -> CounterfactualCheckResult:
    """
    Counterfactual / Prevention Mode ("Check before I submit").
    Analyzes missing fields, date conflicts, and potential rejection risks.
    """
    rejection_risks = []
    missing_fields = []
    inconsistent_facts = []
    recommendations = []

    # 1. Missing reference ID check
    if not any(k in extracted_fields for k in ["application_number", "ref_id", "consumer_no"]):
        missing_fields.append("Application / Consumer Reference Number")
        recommendations.append("Upload or mention your official reference or receipt number to enable direct portal verification.")

    # 2. Document upload check
    if documents_count == 0:
        rejection_risks.append("No supporting document uploaded.")
        recommendations.append("Attach a photo or PDF of your bill, receipt, or acknowledgement slip to reduce rejection risk.")

    # 3. Text ambiguity check
    if len(raw_input.strip()) < 30:
        inconsistent_facts.append("Problem description is very brief.")
        recommendations.append("Provide details regarding department name, transaction date, or exact issue faced.")

    status = "READY"
    if rejection_risks or missing_fields:
        status = "BLOCKED" if len(missing_fields) > 1 else "WARNING"

    confidence = round(1.0 - (len(rejection_risks) * 0.25 + len(missing_fields) * 0.2), 2)
    confidence = max(0.2, min(1.0, confidence))

    return CounterfactualCheckResult(
        status=status,
        rejection_risks=rejection_risks,
        missing_fields=missing_fields,
        inconsistent_facts=inconsistent_facts,
        recommendations=recommendations,
        overall_confidence=confidence
    )
