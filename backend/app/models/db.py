import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, DateTime, ForeignKey, Integer, Float, Boolean, JSON
)
from sqlalchemy.orm import relationship
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    full_name = Column(String(255), nullable=False, default="Citizen User")
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    preferred_language = Column(String(20), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)

    cases = relationship("Case", back_populates="user", cascade="all, delete-orphan")

class Case(Base):
    __tablename__ = "cases"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    title = Column(String(255), nullable=False, default="Citizen Grievance Case")
    raw_input = Column(Text, nullable=False)
    normalized_problem = Column(Text, nullable=True)
    domain = Column(String(100), default="General Citizen")
    intent = Column(String(100), default="Investigation")
    language = Column(String(20), default="en")
    urgency = Column(String(20), default="MEDIUM") # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String(50), default="CREATED") # CREATED, UNDERSTANDING, INVESTIGATING, PENDING_APPROVAL, EXECUTING, VERIFYING, RESOLVED, PARTIALLY_RESOLVED, UNVERIFIED, FAILED
    risk_level = Column(String(20), default="LOW") # LOW, MEDIUM, HIGH, CRITICAL
    confidence_score = Column(Float, default=0.0)
    resolution_score = Column(Float, default=0.0)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="cases")
    messages = relationship("CaseMessage", back_populates="case", cascade="all, delete-orphan")
    entities = relationship("CaseEntity", back_populates="case", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="case", cascade="all, delete-orphan")
    evidence_items = relationship("Evidence", back_populates="case", cascade="all, delete-orphan")
    hypotheses = relationship("Hypothesis", back_populates="case", cascade="all, delete-orphan")
    plans = relationship("Plan", back_populates="case", cascade="all, delete-orphan")
    tool_calls = relationship("ToolCall", back_populates="case", cascade="all, delete-orphan")
    actions = relationship("Action", back_populates="case", cascade="all, delete-orphan")
    approvals = relationship("Approval", back_populates="case", cascade="all, delete-orphan")
    verification_results = relationship("VerificationResult", back_populates="case", cascade="all, delete-orphan")
    audit_events = relationship("AuditEvent", back_populates="case", cascade="all, delete-orphan")

class CaseMessage(Base):
    __tablename__ = "case_messages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    case_id = Column(String(36), ForeignKey("cases.id"), nullable=False)
    sender = Column(String(50), nullable=False) # user, agent, system
    content = Column(Text, nullable=False)
    message_type = Column(String(50), default="text") # text, voice_transcript, document_attachment, alert
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="messages")

class CaseEntity(Base):
    __tablename__ = "case_entities"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    case_id = Column(String(36), ForeignKey("cases.id"), nullable=False)
    entity_type = Column(String(100), nullable=False) # application_number, name, date, amount, portal, location
    entity_value = Column(String(255), nullable=False)
    confidence = Column(Float, default=1.0)
    source = Column(String(100), default="intake")
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="entities")

class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    case_id = Column(String(36), ForeignKey("cases.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    mime_type = Column(String(100), nullable=False)
    file_size = Column(Integer, default=0)
    document_type = Column(String(100), default="UNKNOWN") # bill, certificate, application, receipt, identity
    status = Column(String(50), default="UPLOADED") # UPLOADED, PROCESSED, ERROR
    ocr_text = Column(Text, nullable=True)
    extracted_fields = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="documents")
    extractions = relationship("DocumentExtraction", back_populates="document", cascade="all, delete-orphan")

class DocumentExtraction(Base):
    __tablename__ = "document_extractions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False)
    field_name = Column(String(100), nullable=False)
    field_value = Column(Text, nullable=False)
    confidence = Column(Float, default=1.0)
    bounding_box = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="extractions")

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    case_id = Column(String(36), ForeignKey("cases.id"), nullable=False)
    source_type = Column(String(100), nullable=False) # official_api, web_research, document_ocr, database, user_input
    source_title = Column(String(255), nullable=False)
    source_url = Column(String(512), nullable=True)
    claim_supported = Column(Text, nullable=False)
    content_reference = Column(Text, nullable=True)
    confidence = Column(Float, default=1.0)
    status = Column(String(50), default="CONFIRMED") # CONFIRMED, SUPPORTING, CONTRADICTING, UNVERIFIED, STALE
    retrieved_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="evidence_items")

class Hypothesis(Base):
    __tablename__ = "hypotheses"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    case_id = Column(String(36), ForeignKey("cases.id"), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), default="PROPOSED") # PROPOSED, CONFIRMED, REJECTED, UNVERIFIED
    confidence = Column(Float, default=0.5)
    supporting_evidence_ids = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="hypotheses")

class Plan(Base):
    __tablename__ = "plans"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    case_id = Column(String(36), ForeignKey("cases.id"), nullable=False)
    objective = Column(Text, nullable=False)
    status = Column(String(50), default="ACTIVE") # ACTIVE, COMPLETED, REPLANNED, FAILED
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="plans")
    steps = relationship("PlanStep", back_populates="plan", cascade="all, delete-orphan")

class PlanStep(Base):
    __tablename__ = "plan_steps"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    plan_id = Column(String(36), ForeignKey("plans.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    action_type = Column(String(100), nullable=False)
    required_tool = Column(String(100), nullable=True)
    risk_level = Column(String(20), default="LOW")
    status = Column(String(50), default="PENDING") # PENDING, IN_PROGRESS, COMPLETED, FAILED, SKIPPED
    result_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    plan = relationship("Plan", back_populates="steps")

class ToolCall(Base):
    __tablename__ = "tool_calls"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    case_id = Column(String(36), ForeignKey("cases.id"), nullable=False)
    tool_name = Column(String(100), nullable=False)
    arguments = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)
    status = Column(String(50), default="SUCCESS") # SUCCESS, FAILED, TIMEOUT, PERMISSION_DENIED
    error_message = Column(Text, nullable=True)
    duration_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="tool_calls")

class Action(Base):
    __tablename__ = "actions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    case_id = Column(String(36), ForeignKey("cases.id"), nullable=False)
    action_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    risk_level = Column(String(20), default="LOW") # LOW, MEDIUM, HIGH, CRITICAL
    requires_approval = Column(Boolean, default=False)
    status = Column(String(50), default="PREPARED") # PREPARED, AWAITING_APPROVAL, EXECUTING, EXECUTED, FAILED, REJECTED
    payload = Column(JSON, nullable=True)
    output_result = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="actions")

class Approval(Base):
    __tablename__ = "approvals"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    case_id = Column(String(36), ForeignKey("cases.id"), nullable=False)
    action_id = Column(String(36), ForeignKey("actions.id"), nullable=True)
    title = Column(String(255), nullable=False)
    reason = Column(Text, nullable=False)
    risk_level = Column(String(20), default="MEDIUM")
    status = Column(String(50), default="PENDING") # PENDING, APPROVED, REJECTED
    approved_by = Column(String(100), nullable=True)
    decision_notes = Column(Text, nullable=True)
    requested_at = Column(DateTime, default=datetime.utcnow)
    decided_at = Column(DateTime, nullable=True)

    case = relationship("Case", back_populates="approvals")

class VerificationResult(Base):
    __tablename__ = "verification_results"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    case_id = Column(String(36), ForeignKey("cases.id"), nullable=False)
    verification_type = Column(String(100), nullable=False) # deterministic_rules, schema_validation, state_transition, document_consistency
    status = Column(String(50), default="PASSED") # PASSED, FAILED, WARNING
    details = Column(JSON, nullable=True)
    verified_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="verification_results")

class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    case_id = Column(String(36), ForeignKey("cases.id"), nullable=False)
    event_type = Column(String(100), nullable=False) # CaseCreated, IntentDetected, ToolCalled, EvidenceAdded, ActionExecuted, VerificationCompleted, CaseResolved
    actor = Column(String(100), default="SYSTEM")
    payload = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="audit_events")

class IntegrationStatus(Base):
    __tablename__ = "integrations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(255), nullable=False)
    status = Column(String(50), default="CONNECTED") # CONNECTED, DEGRADED, NOT_CONFIGURED, ERROR
    capabilities = Column(JSON, nullable=True)
    last_health_check = Column(DateTime, default=datetime.utcnow)
    error_message = Column(Text, nullable=True)
