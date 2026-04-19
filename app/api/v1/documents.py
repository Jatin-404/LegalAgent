import uuid
from fastapi import APIRouter, Depends, File, Form, UploadFile, Query, status
from app.models.document import (
    DocumentType,
    DocumentUploadResponse,
    DocumentMetadata,
    DocumentListResponse,
    DocumentStatus,
)
from app.services.ingestion import IngestionService
from app.dependencies import get_ingestion_service
from app.core.exceptions import UnsupportedFileTypeError, FileTooLargeError
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword",
    "text/plain",
    "text/html",
    "message/rfc822",
}


@router.post(
    "",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Upload a legal document for processing",
)
async def upload_document(
    file: UploadFile = File(...),
    document_type: DocumentType = Form(DocumentType.CONTRACT),
    ingestion_svc: IngestionService = Depends(get_ingestion_service),
) -> DocumentUploadResponse:
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise UnsupportedFileTypeError(f"Content type '{file.content_type}' is not supported.")

    content = await file.read()
    if len(content) > settings.max_upload_size_bytes:
        raise FileTooLargeError(
            f"File exceeds the {settings.max_upload_size_mb}MB limit."
        )

    result = await ingestion_svc.ingest(
        filename=file.filename or "unknown",
        content=content,
        content_type=file.content_type or "application/octet-stream",
        document_type=document_type,
    )
    return result


@router.get(
    "",
    response_model=DocumentListResponse,
    summary="List all ingested documents",
)
async def list_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: DocumentStatus | None = Query(None),
    document_type: DocumentType | None = Query(None),
    ingestion_svc: IngestionService = Depends(get_ingestion_service),
) -> DocumentListResponse:
    return await ingestion_svc.list_documents(
        page=page,
        page_size=page_size,
        status_filter=status,
        type_filter=document_type,
    )


@router.get(
    "/{document_id}",
    response_model=DocumentMetadata,
    summary="Get document metadata",
)
async def get_document(
    document_id: uuid.UUID,
    ingestion_svc: IngestionService = Depends(get_ingestion_service),
) -> DocumentMetadata:
    return await ingestion_svc.get_document(document_id)


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a document and its vectors",
)
async def delete_document(
    document_id: uuid.UUID,
    ingestion_svc: IngestionService = Depends(get_ingestion_service),
) -> None:
    await ingestion_svc.delete_document(document_id)