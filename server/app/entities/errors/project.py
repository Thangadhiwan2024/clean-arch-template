"""Project-related errors."""

from app.entities.errors.base import BaseEntityError


class ProjectNotFoundError(BaseEntityError):
    """Error raised when a project is not found."""

    def __init__(self, project_id: str):
        """Initialize the error."""
        self.project_id = project_id
        super().__init__(f"Project with ID '{project_id}' not found.")


class ProjectNameExistsError(BaseEntityError):
    """Error raised when a project with the same name already exists."""

    def __init__(self, project_name: str):
        """Initialize the error."""
        self.project_name = project_name
        super().__init__(f"Project with name '{project_name}' already exists.")


class InvalidProjectStateError(BaseEntityError):
    """Error raised when an invalid state transition is attempted."""

    def __init__(self, current_state: str, requested_state: str):
        """Initialize the error."""
        self.current_state = current_state
        self.requested_state = requested_state
        super().__init__(
            f"Invalid state transition from '{current_state}' to '{requested_state}'."
        )
