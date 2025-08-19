"""Project use cases."""

from typing import Optional

from app.entities.models.project import Project, ProjectState
from app.entities.repositories.project import ProjectRepositoryInterface
from app.use_cases.dto.project import (
    ProjectDTO,
    ProjectUpdateDTO,
    ProjectListRequestDTO,
    ProjectListResponseDTO,
)
from app.use_cases.errors.project import ProjectNotFoundError
from app.use_cases.mappers.project import ProjectMapper


class ProjectService:
    """Service for project operations."""

    def __init__(self, project_repository: ProjectRepositoryInterface):
        """Initialize the project service."""
        self.project_repository = project_repository

    async def create_project(
        self, name: str, description: Optional[str] = None, state: ProjectState = ProjectState.PLANNED
    ) -> ProjectDTO:
        """Create a new project."""
        project = await self.project_repository.create_project(
            name=name,
            description=description,
            state=state,
        )
        return ProjectMapper.entity_to_dto(project)

    async def get_project_by_id(self, project_id: str) -> ProjectDTO:
        """Get a project by ID."""
        project = await self.project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(project_id)
        return ProjectMapper.entity_to_dto(project)

    async def get_projects(
        self, request: ProjectListRequestDTO
    ) -> ProjectListResponseDTO:
        """Get a list of projects."""
        # Get the projects with pagination
        projects = await self.project_repository.get_projects(
            skip=request.skip,
            limit=request.limit,
            state=request.state,
        )

        # Get the total count
        total = await self.project_repository.count_projects(state=request.state)

        # Return the response
        return ProjectMapper.create_list_response(
            total=total,
            skip=request.skip,
            limit=request.limit,
            entities=projects,
        )

    async def update_project(
        self, project_id: str, update_data: ProjectUpdateDTO
    ) -> ProjectDTO:
        """Update an existing project."""
        # Check if the project exists
        existing_project = await self.project_repository.get_project_by_id(project_id)
        if existing_project is None:
            raise ProjectNotFoundError(project_id)

        # Update the project
        updated_project = await self.project_repository.update_project(
            project_id=project_id,
            name=update_data.name,
            description=update_data.description,
            state=update_data.state,
        )

        # Since we already checked existence, this should not be None
        assert updated_project is not None
        return ProjectMapper.entity_to_dto(updated_project)

    async def delete_project(self, project_id: str) -> bool:
        """Delete a project."""
        # Check if the project exists
        existing_project = await self.project_repository.get_project_by_id(project_id)
        if existing_project is None:
            raise ProjectNotFoundError(project_id)

        # Delete the project
        success = await self.project_repository.delete_project(project_id)
        return success
