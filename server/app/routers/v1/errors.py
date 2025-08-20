"""Global error handlers for the application."""

import logging
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.entities.errors.project import (
    ProjectNotFoundError as EntityProjectNotFoundError,
    ProjectNameExistsError as EntityProjectNameExistsError,
    InvalidProjectStateError as EntityInvalidProjectStateError,
)
from app.use_cases.errors.project import (
    ProjectValidationError,
    ProjectOperationNotAllowedError,
    ProjectLimitExceededError,
)
from app.infrastructures.errors.database import (
    DatabaseConnectionError,
    DatabaseQueryError,
    EntityNotFoundInDBError,
)
from app.shared.utils.logging import get_logger

logger = get_logger(__name__)


def log_unexpected_error(error: Exception, request: Request = None) -> None:
    """Log unexpected errors with stack trace for debugging."""
    error_type = type(error)
    error_message = f"Unhandled exception: {error_type.__name__}: {str(error)}"
    
    # Use structured logging if request is available
    if request:
        logger.error(error_message, request=request, exc_info=True)
    else:
        logger.error(error_message, exc_info=True)


def setup_error_handlers(app: FastAPI) -> None:
    """Set up global exception handlers for common errors."""
    
    # Entity errors
    @app.exception_handler(EntityProjectNotFoundError)
    async def entity_project_not_found_handler(_request: Request, exc: EntityProjectNotFoundError):
        """Handle project not found errors."""
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )
    
    @app.exception_handler(EntityProjectNameExistsError)
    async def entity_project_name_exists_handler(_request: Request, exc: EntityProjectNameExistsError):
        """Handle project name exists errors."""
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )
    
    @app.exception_handler(EntityInvalidProjectStateError)
    async def entity_invalid_project_state_handler(_request: Request, exc: EntityInvalidProjectStateError):
        """Handle invalid project state errors."""
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )
    
    # Use case errors
    @app.exception_handler(ProjectValidationError)
    async def project_validation_error_handler(_request: Request, exc: ProjectValidationError):
        """Handle project validation errors."""
        return JSONResponse(
            status_code=400,
            content={
                "detail": str(exc),
                "error_data": {"validation_errors": exc.validation_errors} if hasattr(exc, "validation_errors") else None
            },
        )
    
    @app.exception_handler(ProjectOperationNotAllowedError)
    async def project_operation_not_allowed_handler(_request: Request, exc: ProjectOperationNotAllowedError):
        """Handle operation not allowed errors."""
        return JSONResponse(
            status_code=403,
            content={
                "detail": str(exc),
                "error_data": {"operation": exc.operation, "reason": exc.reason} if hasattr(exc, "operation") else None
            },
        )
    
    @app.exception_handler(ProjectLimitExceededError)
    async def project_limit_exceeded_handler(_request: Request, exc: ProjectLimitExceededError):
        """Handle project limit exceeded errors."""
        return JSONResponse(
            status_code=403,
            content={
                "detail": str(exc),
                "error_data": {"user_id": exc.user_id, "limit": exc.limit} if hasattr(exc, "user_id") else None
            },
        )
    
    # Database errors
    @app.exception_handler(DatabaseConnectionError)
    async def database_connection_error_handler(_request: Request, exc: DatabaseConnectionError):
        """Handle database connection errors."""
        return JSONResponse(
            status_code=503,
            content={"detail": f"Database connection error: {str(exc)}"},
        )
    
    @app.exception_handler(DatabaseQueryError)
    async def database_query_error_handler(_request: Request, exc: DatabaseQueryError):
        """Handle database query errors."""
        return JSONResponse(
            status_code=500,
            content={"detail": f"Database query error: {str(exc)}"},
        )
    
    @app.exception_handler(EntityNotFoundInDBError)
    async def entity_not_found_in_db_handler(_request: Request, exc: EntityNotFoundInDBError):
        """Handle entity not found in database errors."""
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )
