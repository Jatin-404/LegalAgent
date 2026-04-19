from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class LegalAIBaseError(Exception):
    """Base for all domain errors."""
    status_code: int = 500
    detail: str = "An unexpected error occurred."

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.__class__.detail
        super().__init__(self.detail)


class DocumentNotFoundError(LegalAIBaseError):
    status_code = 404
    detail = "Document not found."


class DocumentProcessingError(LegalAIBaseError):
    status_code = 422
    detail = "Failed to process document."


class UnsupportedFileTypeError(LegalAIBaseError):
    status_code = 415
    detail = "File type not supported."


class FileTooLargeError(LegalAIBaseError):
    status_code = 413
    detail = "File exceeds maximum allowed size."


class PlaybookNotFoundError(LegalAIBaseError):
    status_code = 404
    detail = "Playbook not found."


class AnalysisNotReadyError(LegalAIBaseError):
    status_code = 202
    detail = "Analysis is still in progress."


class LLMUnavailableError(LegalAIBaseError):
    status_code = 503
    detail = "LLM service is currently unavailable."


class VectorStoreError(LegalAIBaseError):
    status_code = 503
    detail = "Vector store operation failed."


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(LegalAIBaseError)
    async def domain_exception_handler(
        request: Request, exc: LegalAIBaseError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.__class__.__name__, "detail": exc.detail},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "InternalServerError", "detail": str(exc)},
        )