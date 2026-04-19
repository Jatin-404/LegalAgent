import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class PlaybookRule(BaseModel):
    rule_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    clause_type: str
    description: str
    is_required: bool = False
    fallback_position: str | None = None
    red_flags: list[str] = []
    preferred_language: str | None = None


class PlaybookCreate(BaseModel):
    name: str
    description: str | None = None
    document_type: str = "contract"
    rules: list[PlaybookRule] = []


class PlaybookResponse(BaseModel):
    playbook_id: uuid.UUID
    name: str
    description: str | None
    document_type: str
    rules: list[PlaybookRule]
    rule_count: int
    created_at: datetime
    updated_at: datetime


class PlaybookListResponse(BaseModel):
    items: list[PlaybookResponse]
    total: int