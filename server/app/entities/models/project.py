"""Project related entities for the Project Management Service."""

from enum import Enum
from typing import Optional

from pydantic import Field

from app.entities.models.base import BaseEntity


class ProjectState(str, Enum):
    """Enum representing possible states of a project."""

    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Project(BaseEntity):
    """Entity representing a project."""

    name: str
    description: Optional[str] = None
    state: ProjectState = ProjectState.PLANNED
