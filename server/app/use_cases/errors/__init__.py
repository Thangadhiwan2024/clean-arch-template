"""
Error integration module for use cases.

This module re-exports domain errors from entities and adds use case specific errors.
This helps use case code to import all errors from one place.
"""

# Re-export domain errors
from app.entities.errors.project import (
    ProjectNotFoundError,
    ProjectNameExistsError,
    InvalidProjectStateError
)

# Import use case specific errors
from app.use_cases.errors.project import (
    ProjectValidationError,
    ProjectOperationNotAllowedError,
    ProjectLimitExceededError
)

__all__ = [
    # Domain errors
    'ProjectNotFoundError',
    'ProjectNameExistsError',
    'InvalidProjectStateError',
    
    # Use case errors
    'ProjectValidationError',
    'ProjectOperationNotAllowedError',
    'ProjectLimitExceededError'
]
