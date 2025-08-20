"""Routers for project operations."""

import logging
import asyncio
from fastapi import APIRouter, Depends, HTTPException, status, Request

from app.entities.models.project import ProjectState

from app.use_cases.errors import (
    ProjectNotFoundError,
    ProjectNameExistsError,
    InvalidProjectStateError,
)
from app.infrastructures.errors.database import (
    DatabaseConnectionError,
    DatabaseQueryError,
    EntityNotFoundInDBError,
)
from app.routers.v1.schemas.project import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectUpdateRequest,
    ProjectListRequest,
    ProjectListResponse,
)
from app.routers.v1.schemas.errors import PROJECT_RESPONSES
from app.routers.v1.services import get_project_service
from app.routers.v1.mappers import map_project_to_response, map_project_list_to_response
from app.use_cases.project import ProjectService
from app.shared.utils.logging import get_logger
from app.routers.v1.errors import log_unexpected_error

project_router = APIRouter(prefix="/project", tags=["project"])
logger = get_logger(__name__)


@project_router.post(
    "/", 
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    responses=PROJECT_RESPONSES,
)
async def create_project(
    request: Request,
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
        return map_project_to_response(project)
    except (ProjectNotFoundError, ProjectNameExistsError, InvalidProjectStateError,
            DatabaseConnectionError, DatabaseQueryError, EntityNotFoundInDBError,
            asyncio.CancelledError):
        # Let the global exception handlers handle these known error types
        raise
    except Exception as error:
        # For unexpected errors, log and raise a generic error
        log_unexpected_error(error, request)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        ) from error


@project_router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    responses=PROJECT_RESPONSES,
)
async def get_project(
    request: Request,
    project_id: str, 
    project_service: ProjectService = Depends(get_project_service)
) -> ProjectResponse:
    """Retrieve a project by its ID."""
    try:
        project = await project_service.get_project_by_id(project_id)
        return map_project_to_response(project)
    except (ProjectNotFoundError, ProjectNameExistsError, InvalidProjectStateError,
            DatabaseConnectionError, DatabaseQueryError, EntityNotFoundInDBError, 
            asyncio.CancelledError):
        # Let the global exception handlers handle these known error types
        raise
    except Exception as error:
        # For unexpected errors, log and raise a generic error
        log_unexpected_error(error, request)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        ) from error


@project_router.get(
    "/",
    response_model=ProjectListResponse,
    responses=PROJECT_RESPONSES,
)
async def list_projects(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    state: ProjectState = None,
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectListResponse:
    """Retrieve a list of projects with optional filtering by state."""
    try:
        req = ProjectListRequest(skip=skip, limit=limit, state=state)
        list_response = await project_service.get_projects(req)
        return map_project_list_to_response(list_response)
    except (InvalidProjectStateError, DatabaseConnectionError, DatabaseQueryError,
            asyncio.CancelledError):
        # Let the global exception handlers handle these known error types
        raise
    except Exception as error:
        # For unexpected errors, log and raise a generic error
        log_unexpected_error(error, request)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        ) from error


@project_router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    responses=PROJECT_RESPONSES,
)
async def update_project(
    request: Request,
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
        return map_project_to_response(project)
    except (ProjectNotFoundError, ProjectNameExistsError, InvalidProjectStateError, 
            DatabaseConnectionError, DatabaseQueryError, EntityNotFoundInDBError,
            asyncio.CancelledError):
        # Let the global exception handlers handle these known error types
        raise
    except Exception as error:
        # For unexpected errors, log and raise a generic error
        log_unexpected_error(error, request)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        ) from error


@project_router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=PROJECT_RESPONSES,
)
async def delete_project(
    request: Request,
    project_id: str,
    project_service: ProjectService = Depends(get_project_service),
) -> None:
    """Delete a project by its ID."""
    try:
        await project_service.delete_project(project_id)
    except (ProjectNotFoundError, DatabaseConnectionError, DatabaseQueryError,
            EntityNotFoundInDBError, asyncio.CancelledError):
        # Let the global exception handlers handle these known error types
        raise
    except Exception as error:
        # For unexpected errors, log and raise a generic error
        log_unexpected_error(error, request)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        ) from error
