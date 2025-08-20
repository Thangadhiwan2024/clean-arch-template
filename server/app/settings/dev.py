"""Dev settings for the project management service."""

from app.settings.base import ProjectManagementBaseSettings


class ProjectManagementDevSettings(ProjectManagementBaseSettings):
    """Development settings for the project management service."""

    # Environment
    APP_ENV: str = "dev"

    # Database settings
    DATABASE_URL: str = "sqlite+aiosqlite:///./project_management.db"
    LOG_DB_QUERIES: bool = True

    # Logging settings
    LOG_LEVEL: str = "DEBUG"

    # App Settings
    APP_NAME: str = "Project Management Service"
    PROJECT_MANAGEMENT_SERVICE_DEBUG: bool = True
