"""Configuration settings for the project management service."""

from functools import lru_cache

from app.settings.base import ProjectManagementBaseSettings
from app.settings.dev import ProjectManagementDevSettings


@lru_cache
def get_settings() -> ProjectManagementBaseSettings | ProjectManagementDevSettings:
    """Get the appropriate settings based on the environment."""
    if ProjectManagementBaseSettings().APP_ENV == "dev":
        return ProjectManagementDevSettings()
    else:
        return ProjectManagementBaseSettings()
