# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run development server
uv run uvicorn app.main:app --reload

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=app

# Lint
uv run ruff check

# Type check
uv run mypy

# Run single test
uv run pytest -k test_name
```

## Architecture

**Framework**: FastAPI backend for legal document analysis with async processing pipeline.

**Layer structure**:
```
app/
├── main.py              # App factory with lifespan (init DB, logging)
├── api/v1/              # REST endpoints (health, documents, analysis, playbooks)
├── core/                # Config (pydantic-settings), logging (structlog), exceptions
├── models/              # Pydantic schemas for request/response
├── services/            # Business logic (ingestion, analysis)
├── db/                  # Database session (SQLAlchemy async + PostgreSQL)
└── workers/             # Celery tasks for background processing
```

**Key components**:
- **Document ingestion**: Upload → S3 storage → parsing (docling/unstructured) → embedding (Ollama) → vector store (Qdrant)
- **Analysis pipeline**: Async Celery workers process documents using LLM (Ollama) for clause extraction, risk flagging, redline suggestions
- **Retrieval**: RAG-based context retrieval from Qdrant vector store

**External services** (configured via `.env`):
- PostgreSQL (database), Redis (Celery broker), Qdrant (vectors), Ollama (LLM/embeddings), MinIO/S3 (document storage)

**Error handling**: Custom exception hierarchy in `app/core/exceptions.py` with domain-specific errors (DocumentNotFoundError, AnalysisNotReadyError, etc.) registered via `register_exception_handlers()`.
