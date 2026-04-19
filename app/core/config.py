from functools import lru_cache
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_debug: bool = False
    secret_key: str = "change-me"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/legal_ai"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Qdrant
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection: str = "legal_documents"

    # Ollama / LLM
    ollama_base_url: str = "http://localhost:11434"
    ollama_extractor_model: str = "mistral:7b"
    ollama_analyst_model: str = "mixtral:8x7b"
    ollama_embed_model: str = "nomic-embed-text"

    # S3 / MinIO
    s3_endpoint_url: str = "http://localhost:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket_name: str = "legal-documents"
    s3_region: str = "us-east-1"

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # Processing limits
    max_upload_size_mb: int = 50
    max_chunk_size: int = 1024
    chunk_overlap: int = 128
    top_k_retrieval: int = 10

    @field_validator("app_env")
    @classmethod
    def validate_env(cls, v: str) -> str:
        allowed = {"development", "staging", "production"}
        if v not in allowed:
            raise ValueError(f"app_env must be one of {allowed}")
        return v

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()