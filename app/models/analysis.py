import uuid
from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, Field


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AnalysisStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"


class RiskFlag(BaseModel):
    flag_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    clause_type: str
    risk_level: RiskLevel
    description: str
    citation: str
    suggestion: str | None = None
    playbook_rule_id: str | None = None


class MissingClause(BaseModel):
    clause_type: str
    required_by: str
    description: str


class RedlineSuggestion(BaseModel):
    clause_id: uuid.UUID
    original_text: str
    suggested_text: str
    rationale: str
    confidence: float = Field(ge=0.0, le=1.0)


class AnalysisResult(BaseModel):
    analysis_id: uuid.UUID
    document_id: uuid.UUID
    playbook_id: uuid.UUID | None = None
    status: AnalysisStatus
    overall_risk: RiskLevel | None = None
    summary: str | None = None
    risk_flags: list[RiskFlag] = []
    missing_clauses: list[MissingClause] = []
    redline_suggestions: list[RedlineSuggestion] = []
    retrieved_context_ids: list[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None


class AnalysisRequest(BaseModel):
    document_id: uuid.UUID
    playbook_id: uuid.UUID | None = None
    focus_areas: list[str] = Field(
        default=[],
        description="Optional list of clause types to focus on, e.g. ['termination', 'liability']",
    )


class AnalysisStatusResponse(BaseModel):
    analysis_id: uuid.UUID
    document_id: uuid.UUID
    status: AnalysisStatus
    progress_pct: int = Field(ge=0, le=100)
    message: str | None = None