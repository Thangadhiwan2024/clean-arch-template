"""Base error for the project management service use cases."""


class ProjectManagementUseCaseError(Exception):
    """Base class for all use case errors."""

    def __init__(self, message: str):
        """Initialize the error with a message."""
        super().__init__(message)
        self.message = message
