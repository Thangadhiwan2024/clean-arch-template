"""
Utility functions for use cases.
"""

from typing import Dict, List, Optional, Any

from app.entities.models.project import Project
from app.use_cases.dto.project import ProjectOutputDTO


def map_project_to_dto(project: Project) -> ProjectOutputDTO:
    """
    Map a Project entity to a ProjectOutputDTO.
    
    Args:
        project: The project entity to map
    
    Returns:
        The DTO representation of the project
    """
    return ProjectOutputDTO(
        id=project.id,
        name=project.name,
        description=project.description,
        state=project.state,
        created_at=project.created_at,
        updated_at=project.updated_at
    )


def map_projects_to_dtos(projects: List[Project]) -> List[ProjectOutputDTO]:
    """
    Map a list of Project entities to ProjectOutputDTOs.
    
    Args:
        projects: The list of project entities to map
    
    Returns:
        A list of DTO representations of the projects
    """
    return [map_project_to_dto(project) for project in projects]


def build_pagination_response(
    items: List[Any],
    total: int,
    page: int,
    page_size: int
) -> Dict[str, Any]:
    """
    Build a standardized pagination response.
    
    Args:
        items: The items for the current page
        total: The total number of items
        page: The current page number
        page_size: The page size
    
    Returns:
        A dictionary with pagination metadata and items
    """
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    has_next = page < total_pages
    has_prev = page > 1
    
    return {
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_prev": has_prev
        }
    }
