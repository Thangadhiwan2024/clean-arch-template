"""
Initialization file for infrastructure errors.
"""

from app.infrastructures.errors.base import InfrastructureError
from app.infrastructures.errors.database import (
    DatabaseConnectionError,
    DatabaseQueryError,
    EntityNotFoundInDBError
)

__all__ = [
    'InfrastructureError',
    'DatabaseConnectionError',
    'DatabaseQueryError',
    'EntityNotFoundInDBError'
]
