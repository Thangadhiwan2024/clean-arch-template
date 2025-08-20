"""Repository interface for projects."""

from abc import ABC, abstractmethod
from typing import Optional, List

from app.entities.models.project import Project, ProjectState


class ProjectRepositoryInterface(ABC):
    """Interface for project repository."""

    @abstractmethod
    async def create_project(self, name: str, description: Optional[str] = None, 
                             state: ProjectState = ProjectState.PLANNED) -> Project:
        """Create a new project with the provided details."""
        pass

    @abstractmethod
    async def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """Retrieve a project by its ID."""
        pass

    @abstractmethod
    async def get_projects(self, skip: int = 0, limit: int = 100, 
                           state: Optional[ProjectState] = None) -> List[Project]:
        """Retrieve projects with pagination and optional filtering by state."""
        pass

    @abstractmethod
    async def update_project(self, project_id: str, name: Optional[str] = None, 
                             description: Optional[str] = None, 
                             state: Optional[ProjectState] = None) -> Optional[Project]:
        """Update an existing project with the provided data."""
        pass

    @abstractmethod
    async def delete_project(self, project_id: str) -> bool:
        """Delete a project by its ID. Returns True if successful, False otherwise."""
        pass

    @abstractmethod
    async def count_projects(self, state: Optional[ProjectState] = None) -> int:
        """Count the total number of projects, with optional filtering by state."""
        pass
