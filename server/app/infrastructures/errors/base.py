"""
Base error class for infrastructure layer.
"""


class InfrastructureError(Exception):
    """Base class for all infrastructure-related exceptions."""

    def __init__(self, message: str):
        """Initialize the error with a message."""
        super().__init__(message)
        self.message = message
