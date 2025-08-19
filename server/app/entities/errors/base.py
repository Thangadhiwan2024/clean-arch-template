"""Base exception class for the Project Management Service entities."""


class BaseEntityError(Exception):
    """Base class for all entity-related exceptions in the Project Management Service."""

    def __init__(self, message: str):
        """Initialize the base entity error with a message."""
        super().__init__(message)
        self.message = message
