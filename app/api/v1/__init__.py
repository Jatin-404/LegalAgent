from fastapi import APIRouter
from app.api.v1 import documents, analysis, playbooks, health

router = APIRouter()

router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(documents.router, prefix="/documents", tags=["documents"])
router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
router.include_router(playbooks.router, prefix="/playbooks", tags=["playbooks"])