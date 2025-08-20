"""
Initialization file for entity utilities.
"""

from app.entities.utils.project import (
    validate_project_name,
    is_valid_state_transition
)

__all__ = [
    'validate_project_name',
    'is_valid_state_transition'
]
