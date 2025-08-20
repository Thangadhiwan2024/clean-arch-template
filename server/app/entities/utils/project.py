"""
Utility functions for project domain operations.
"""

from app.entities.constants.project import (
    PROJECT_NAME_MIN_LENGTH,
    PROJECT_NAME_MAX_LENGTH
)
from app.entities.models.project import Project, ProjectState


def validate_project_name(name: str) -> bool:
    """
    Validate a project name according to domain rules.
    
    Args:
        name: The project name to validate
    
    Returns:
        True if the name is valid, False otherwise
    """
    return len(name) >= PROJECT_NAME_MIN_LENGTH and len(name) <= PROJECT_NAME_MAX_LENGTH


def is_valid_state_transition(current_state: ProjectState, new_state: ProjectState) -> bool:
    """
    Check if a project state transition is valid according to business rules.
    
    Args:
        current_state: The current state of the project
        new_state: The requested new state
    
    Returns:
        True if the transition is valid, False otherwise
    """
    # Define allowed transitions
    allowed_transitions = {
        ProjectState.PLANNED: [ProjectState.IN_PROGRESS, ProjectState.CANCELLED],
        ProjectState.IN_PROGRESS: [ProjectState.COMPLETED, ProjectState.CANCELLED],
        ProjectState.COMPLETED: [ProjectState.IN_PROGRESS],  # Allow reopening completed projects
        ProjectState.CANCELLED: [ProjectState.PLANNED]  # Allow restarting cancelled projects
    }
    
    # Check if the transition is allowed
    return new_state in allowed_transitions.get(current_state, [])
