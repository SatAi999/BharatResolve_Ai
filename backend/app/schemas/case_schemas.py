from typing import List, Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field

class EntitySchema(BaseModel):
    entity_type: str = "general"
    entity_value: str = ""
    confidence: float = 1.0
    source: str = "intake"

class CaseCreate(BaseModel):
    raw_input: str = Field(..., description="The user's problem description in text, Hinglish, or Indian language")
    language: str = Field(default="en", description="Detected or preferred language: en, hi, hinglish, etc.")
    user_name: Optional[str] = "Citizen User"
    voice_file_path: Optional[str] = None

class CaseIntent(BaseModel):
    domain: str = Field(default="Education", description="Category: GovTech, Education, Financial Services, Utilities, Logistics, Agriculture, Healthcare Admin, Employment, MSME")
    intent: str = Field(default="Status Investigation", description="Primary user goal e.g. Status Investigation, Grievance Preparation, Bill Anomaly, Scholarship Support")
    normalized_problem: str = Field(default="Citizen problem requiring investigation", description="Concise English problem statement")
    urgency: str = Field(default="MEDIUM", description="LOW, MEDIUM, HIGH, CRITICAL")
    extracted_entities: List[EntitySchema] = []
    missing_information: List[str] = []
    detected_language: str = "en"
    ambiguity_flag: bool = False

class EvidenceSchema(BaseModel):
    id: Optional[str] = None
    source_type: str = "web_research"
    source_title: str = "Source"
    source_url: Optional[str] = None
    claim_supported: str = ""
    content_reference: Optional[str] = None
    confidence: float = 1.0
    status: str = "CONFIRMED" # CONFIRMED, SUPPORTING, CONTRADICTING, UNVERIFIED, STALE
    retrieved_at: Optional[datetime] = None

class HypothesisSchema(BaseModel):
    id: Optional[str] = None
    description: str = ""
    status: str = "PROPOSED"
    confidence: float = 0.5
    supporting_evidence_ids: List[str] = []

class PlanStepSchema(BaseModel):
    id: Optional[str] = None
    step_number: int = 1
    title: str = "Step"
    description: Optional[str] = None
    action_type: str = "investigate"
    required_tool: Optional[str] = None
    risk_level: str = "LOW"
    status: str = "PENDING"
    result_summary: Optional[str] = None

class PlanSchema(BaseModel):
    id: Optional[str] = None
    objective: str = "Resolve Case"
    status: str = "ACTIVE"
    steps: List[PlanStepSchema] = []

class ActionSchema(BaseModel):
    id: Optional[str] = None
    action_name: str = "action"
    description: str = ""
    risk_level: str = "LOW"
    requires_approval: bool = False
    status: str = "PREPARED"
    payload: Optional[Dict[str, Any]] = None
    output_result: Optional[Dict[str, Any]] = None

class ApprovalSchema(BaseModel):
    id: str
    case_id: str
    action_id: Optional[str] = None
    title: str
    reason: str
    risk_level: str
    status: str
    approved_by: Optional[str] = None
    decision_notes: Optional[str] = None
    requested_at: datetime

class ApprovalDecision(BaseModel):
    approval_id: str
    decision: str = Field(..., description="APPROVED or REJECTED")
    notes: Optional[str] = None
    approved_by: str = "User"

class VerificationResultSchema(BaseModel):
    id: Optional[str] = None
    verification_type: str = "validation"
    status: str = "PASSED"
    details: Optional[Dict[str, Any]] = None
    verified_at: Optional[datetime] = None

class AuditEventSchema(BaseModel):
    id: Optional[str] = None
    event_type: str = "Event"
    actor: str = "SYSTEM"
    payload: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None

class CounterfactualCheckResult(BaseModel):
    status: str = Field(default="READY", description="READY, WARNING, BLOCKED")
    rejection_risks: List[str] = []
    missing_fields: List[str] = []
    inconsistent_facts: List[str] = []
    recommendations: List[str] = []
    overall_confidence: float = 1.0

class IntegrationHealth(BaseModel):
    name: str
    display_name: str
    status: str
    capabilities: List[str] = []
    last_health_check: datetime
    error_message: Optional[str] = None

class CaseResponse(BaseModel):
    id: str
    title: str
    raw_input: str
    normalized_problem: Optional[str] = None
    domain: str = "General Citizen"
    intent: str = "Investigation"
    language: str = "en"
    urgency: str = "MEDIUM"
    status: str = "CREATED"
    risk_level: str = "LOW"
    confidence_score: float = 0.0
    resolution_score: float = 0.0
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    messages: List[Dict[str, Any]] = []
    entities: List[EntitySchema] = []
    evidence_items: List[EvidenceSchema] = []
    hypotheses: List[HypothesisSchema] = []
    plans: List[PlanSchema] = []
    actions: List[ActionSchema] = []
    approvals: List[ApprovalSchema] = []
    verification_results: List[VerificationResultSchema] = []
    audit_events: List[AuditEventSchema] = []
