"""Routers for project operations."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status

from app.entities.models.project import ProjectState
from app.entities.errors.project import (
    ProjectNotFoundError as EntityProjectNotFoundError,
    ProjectNameExistsError as EntityProjectNameExistsError,
    InvalidProjectStateError as EntityInvalidProjectStateError,
)
from app.use_cases.errors.project import (
    ProjectNotFoundError as UseCaseProjectNotFoundError,
    ProjectNameExistsError as UseCaseProjectNameExistsError,
    InvalidProjectStateTransitionError as UseCaseInvalidStateError,
)
from app.routers.v1.schemas.project import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectUpdateRequest,
    ProjectListRequest,
    ProjectListResponse,
)
from app.routers.v1.schemas.errors import HTTPErrorResponse
from app.routers.v1.services import get_project_service
from app.use_cases.project import ProjectService

project_router = APIRouter(prefix="/project", tags=["project"])


def log_unexpected_error(error: Exception) -> None:
    """Log unexpected errors with stack trace for debugging."""
    error_type = type(error)
    logging.error("Unhandled exception: %s: %s", error_type.__name__, str(error), exc_info=True)


@project_router.post(
    "/", 
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": HTTPErrorResponse,
            "description": "Project name already exists",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HTTPErrorResponse,
            "description": "Internal server error",
        },
    },
)
async def create_project(
    project_request: ProjectCreateRequest, 
    project_service: ProjectService = Depends(get_project_service)
) -> ProjectResponse:
    """Create a new project with the given details."""
    try:
        project = await project_service.create_project(
            name=project_request.name,
            description=project_request.description,
            state=project_request.state,
        )
        return ProjectResponse(**project.model_dump())
    except (EntityProjectNameExistsError, UseCaseProjectNameExistsError) as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error.message,
        ) from error
    except Exception as error:
        log_unexpected_error(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        ) from error


@project_router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": HTTPErrorResponse,
            "description": "Project not found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HTTPErrorResponse,
            "description": "Internal server error",
        },
    },
)
async def get_project(
    project_id: str, 
    project_service: ProjectService = Depends(get_project_service)
) -> ProjectResponse:
    """Retrieve a project by its ID."""
    try:
        project = await project_service.get_project_by_id(project_id)
        return ProjectResponse(**project.model_dump())
    except (EntityProjectNotFoundError, UseCaseProjectNotFoundError) as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error.message,
        ) from error
    except Exception as error:
        log_unexpected_error(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        ) from error


@project_router.get(
    "/",
    response_model=ProjectListResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTPErrorResponse,
            "description": "Invalid project state",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HTTPErrorResponse,
            "description": "Internal server error",
        },
    },
)
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    state: ProjectState = None,
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectListResponse:
    """Retrieve a list of projects with optional filtering by state."""
    try:
        request = ProjectListRequest(skip=skip, limit=limit, state=state)
        list_response = await project_service.get_projects(request)
        return ProjectListResponse(
            total=list_response.total,
            skip=list_response.skip,
            limit=list_response.limit,
            items=[ProjectResponse(**item.model_dump()) for item in list_response.items],
        )
    except (EntityInvalidProjectStateError, UseCaseInvalidStateError) as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error.message,
        ) from error
    except Exception as error:
        log_unexpected_error(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        ) from error


@project_router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": HTTPErrorResponse,
            "description": "Project not found",
        },
        status.HTTP_409_CONFLICT: {
            "model": HTTPErrorResponse,
            "description": "Project name already exists",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTPErrorResponse,
            "description": "Invalid project state transition",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HTTPErrorResponse,
            "description": "Internal server error",
        },
    },
)
async def update_project(
    project_id: str,
    update_data: ProjectUpdateRequest,
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    """Update an existing project with the provided data."""
    try:
        project = await project_service.update_project(
            project_id=project_id,
            update_data=update_data,
        )
        return ProjectResponse(**project.model_dump())
    except (EntityProjectNotFoundError, UseCaseProjectNotFoundError) as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error.message,
        ) from error
    except (EntityProjectNameExistsError, UseCaseProjectNameExistsError) as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error.message,
        ) from error
    except (EntityInvalidProjectStateError, UseCaseInvalidStateError) as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error.message,
        ) from error
    except Exception as error:
        log_unexpected_error(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        ) from error


@project_router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": HTTPErrorResponse,
            "description": "Project not found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HTTPErrorResponse,
            "description": "Internal server error",
        },
    },
)
async def delete_project(
    project_id: str,
    project_service: ProjectService = Depends(get_project_service),
) -> None:
    """Delete a project by its ID."""
    try:
        await project_service.delete_project(project_id)
    except (EntityProjectNotFoundError, UseCaseProjectNotFoundError) as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error.message,
        ) from error
    except Exception as error:
        log_unexpected_error(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        ) from error
