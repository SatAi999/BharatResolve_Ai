from typing import List, Dict, Any
from app.schemas.case_schemas import EvidenceSchema

def evaluate_evidence_graph(evidence_list: List[EvidenceSchema]) -> Dict[str, Any]:
    """
    Evaluates evidence quality, support vs contradiction, and unverified claims.
    """
    if not evidence_list:
        return {
            "completeness_score": 0.0,
            "has_contradictions": False,
            "confirmed_count": 0,
            "unverified_count": 0,
            "status": "UNVERIFIED"
        }

    confirmed = [e for e in evidence_list if e.status == "CONFIRMED"]
    supporting = [e for e in evidence_list if e.status == "SUPPORTING"]
    contradicting = [e for e in evidence_list if e.status == "CONTRADICTING"]
    unverified = [e for e in evidence_list if e.status == "UNVERIFIED"]

    total = len(evidence_list)
    completeness = min(1.0, (len(confirmed) * 1.0 + len(supporting) * 0.7) / max(1, total))

    has_contradiction = len(contradicting) > 0

    return {
        "completeness_score": round(completeness, 2),
        "has_contradictions": has_contradiction,
        "confirmed_count": len(confirmed),
        "supporting_count": len(supporting),
        "contradicting_count": len(contradicting),
        "unverified_count": len(unverified),
        "status": "CONTRADICTED" if has_contradiction else ("CONFIRMED" if completeness > 0.7 else "PARTIAL")
    }
