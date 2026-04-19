import uuid
from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, Field, ConfigDict


class DocumentStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class DocumentType(StrEnum):
    CONTRACT = "contract"
    POLICY = "policy"
    EMAIL = "email"
    TEMPLATE = "template"
    REGULATION = "regulation"
    OTHER = "other"


class DocumentUploadResponse(BaseModel):
    document_id: uuid.UUID
    filename: str
    status: DocumentStatus
    message: str


class DocumentMetadata(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    document_id: uuid.UUID
    filename: str
    document_type: DocumentType
    status: DocumentStatus
    file_size_bytes: int
    page_count: int | None = None
    s3_key: str
    created_at: datetime
    updated_at: datetime


class DocumentListResponse(BaseModel):
    items: list[DocumentMetadata]
    total: int
    page: int
    page_size: int


class ExtractedClause(BaseModel):
    clause_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    clause_type: str
    text: str
    page_number: int | None = None
    confidence: float = Field(ge=0.0, le=1.0)


class ExtractedEntity(BaseModel):
    text: str
    label: str
    start: int
    end: int
    confidence: float = Field(ge=0.0, le=1.0)


class DocumentExtraction(BaseModel):
    document_id: uuid.UUID
    raw_text: str
    clauses: list[ExtractedClause]
    entities: list[ExtractedEntity]
    metadata: dict
    extracted_at: datetime = Field(default_factory=datetime.utcnow)