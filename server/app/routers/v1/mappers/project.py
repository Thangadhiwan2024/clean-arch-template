"""Mapper functions for project-related data transformation."""

from typing import List

from app.entities.models.project import Project
from app.use_cases.dto.project import ProjectDTO, ProjectListResponseDTO
from app.routers.v1.schemas.project import ProjectResponse, ProjectListResponse


def map_project_to_response(project: ProjectDTO) -> ProjectResponse:
    """Map a ProjectDTO to a ProjectResponse schema.
    
    This provides a consistent mapping from domain/application objects to API response schemas.
    """
    return ProjectResponse(**project.model_dump())


def map_project_list_to_response(project_list: ProjectListResponseDTO) -> ProjectListResponse:
    """Map a ProjectListResponseDTO to a ProjectListResponse schema.
    
    This provides a consistent mapping from domain/application objects to API response schemas.
    """
    return ProjectListResponse(
        items=[map_project_to_response(item) for item in project_list.items],
        total=project_list.total,
        skip=project_list.skip,
        limit=project_list.limit,
    )
