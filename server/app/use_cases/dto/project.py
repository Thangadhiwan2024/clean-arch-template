"""Data Transfer Objects for project use cases."""

from typing import Optional
from pydantic import BaseModel

from app.entities.models.project import ProjectState
from app.use_cases.dto.base import BaseDTO


class ProjectDTO(BaseDTO):
    """Data Transfer Object for project information."""

    name: str
    description: Optional[str] = None
    state: ProjectState = ProjectState.PLANNED


class ProjectUpdateDTO(BaseDTO):
    """Data Transfer Object for project update information."""

    name: Optional[str] = None
    description: Optional[str] = None
    state: Optional[ProjectState] = None


class ProjectListRequestDTO(BaseDTO):
    """Data Transfer Object for project list request."""

    skip: int = 0
    limit: int = 100
    state: Optional[ProjectState] = None


class ProjectListResponseDTO(BaseDTO):
    """Data Transfer Object for project list response."""

    total: int
    skip: int
    limit: int
    items: list[ProjectDTO]
