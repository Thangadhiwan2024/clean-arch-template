"""
Initialization file for entity constants.
"""

from app.entities.constants.project import (
    PROJECT_NAME_MIN_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_DESCRIPTION_MAX_LENGTH,
    MAX_PROJECTS_PER_USER,
    MAX_TASKS_PER_PROJECT
)

__all__ = [
    'PROJECT_NAME_MIN_LENGTH',
    'PROJECT_NAME_MAX_LENGTH',
    'PROJECT_DESCRIPTION_MAX_LENGTH',
    'MAX_PROJECTS_PER_USER',
    'MAX_TASKS_PER_PROJECT'
]
