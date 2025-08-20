"""
Database-related errors for the infrastructure layer.
"""

from app.infrastructures.errors.base import InfrastructureError


class DatabaseConnectionError(InfrastructureError):
    """Error raised when a database connection cannot be established."""

    def __init__(self, detail: str = "Failed to connect to the database"):
        """Initialize the error."""
        super().__init__(detail)
        self.detail = detail


class DatabaseQueryError(InfrastructureError):
    """Error raised when a database query fails."""

    def __init__(self, query: str, detail: str = "Database query failed"):
        """Initialize the error."""
        self.query = query
        self.detail = detail
        message = f"{detail}: {query}"
        super().__init__(message)


class EntityNotFoundInDBError(InfrastructureError):
    """Error raised when an entity is not found in the database."""

    def __init__(self, entity_type: str, entity_id: str):
        """Initialize the error."""
        self.entity_type = entity_type
        self.entity_id = entity_id
        message = f"{entity_type} with ID '{entity_id}' not found in the database"
        super().__init__(message)
