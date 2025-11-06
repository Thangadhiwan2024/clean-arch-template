"""Project use case errors.

This module contains errors specific to project use cases that are not
related to domain rules but rather to application-specific concerns.

Domain errors (like ProjectNotFoundError) should be imported from app.entities.errors.project
and used directly in use cases.
"""

from app.use_cases.errors.base import ProjectManagementUseCaseError


class ProjectValidationError(ProjectManagementUseCaseError):
    """Error raised when project data fails validation at the use case level."""

    def __init__(self, message: str, validation_errors: dict = None):
        """Initialize the error."""
        self.validation_errors = validation_errors or {}
        super().__init__(message)


class ProjectOperationNotAllowedError(ProjectManagementUseCaseError):
    """Error raised when an operation is not allowed due to business rules."""

    def __init__(self, operation: str, reason: str):
        """Initialize the error."""
        self.operation = operation
        self.reason = reason
        super().__init__(f"Operation '{operation}' is not allowed: {reason}")


class ProjectLimitExceededError(ProjectManagementUseCaseError):
    """Error raised when a user has reached the maximum number of projects."""

    def __init__(self, user_id: str, limit: int):
        """Initialize the error."""
        self.user_id = user_id
        self.limit = limit
        super().__init__(f"User '{user_id}' has reached the maximum limit of {limit} projects")
