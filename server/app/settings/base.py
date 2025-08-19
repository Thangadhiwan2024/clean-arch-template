"""Base settings for the project management service."""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_TYPES = Literal["dev", "prod", "test"]


class ProjectManagementBaseSettings(BaseSettings):
    """Base settings for the project management service."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Environment
    APP_ENV: ENV_TYPES = "prod"

    # Database settings
    DATABASE_URL: str = "sqlite+aiosqlite:///./project_management.db"
    LOG_DB_QUERIES: bool = False

    # Logging settings
    LOG_LEVEL: str = "INFO"

    # App Settings
    APP_NAME: str = "Project Manager"
    APP_VERSION: str = "1.0.0"
    PROJECT_MANAGEMENT_SERVICE_HOST: str = "0.0.0.0"
    PROJECT_MANAGEMENT_SERVICE_PORT: int = 8000
    PROJECT_MANAGEMENT_SERVICE_DEBUG: bool = False
    ALLOWED_HOSTS: list[str] = ["*"]
    ALLOWED_METHODS: list[str] = ["GET", "POST", "PATCH", "PUT", "DELETE"]
    ALLOWED_HEADERS: list[str] = ["*"]

    # CORS settings
    CORS_ORIGINS: list[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_EXPOSE_HEADERS: list[str] = ["*"]
