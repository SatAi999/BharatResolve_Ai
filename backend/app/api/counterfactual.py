from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.engine.scoring import run_counterfactual_precheck
from app.schemas.case_schemas import CounterfactualCheckResult

router = APIRouter(prefix="/api/counterfactual", tags=["Counterfactual Check"])

class CounterfactualRequest(BaseModel):
    problem_statement: str
    extracted_fields: Optional[Dict[str, Any]] = {}
    documents_count: Optional[int] = 0

@router.post("/check", response_model=CounterfactualCheckResult)
def check_before_submit(payload: CounterfactualRequest):
    """
    Counterfactual / Prevention Mode ("Check before I submit").
    Evaluates missing fields, contradictory dates/names, and rejection risks before filing.
    """
    return run_counterfactual_precheck(
        raw_input=payload.problem_statement,
        extracted_fields=payload.extracted_fields or {},
        documents_count=payload.documents_count or 0
    )
