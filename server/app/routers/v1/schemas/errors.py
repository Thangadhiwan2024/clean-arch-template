"""Schemas for error responses."""

from typing import List, Optional, Any, Dict
from fastapi import status
from pydantic import BaseModel, Field


class ValidationErrorItem(BaseModel):
    """Schema for a single validation error item.
    
    Attributes:
        loc: Location of the validation error, typically path to the invalid field
        msg: Human-readable error message
        type: Type of validation error, e.g., 'invalid_enum_value', 'type_error', etc.
    """
    
    loc: List[str]
    msg: str
    type: str


class ValidationErrorResponse(BaseModel):
    """Schema for validation error responses.
    
    Attributes:
        detail: Summary of the validation error
        errors: List of specific validation errors
    """
    
    detail: str
    errors: List[ValidationErrorItem]


class HTTPErrorResponse(BaseModel):
    """Base schema for HTTP error responses."""

    detail: str
    
    # Optional additional error data that can be included in some cases
    error_data: Optional[Dict[str, Any]] = None


# Common response templates for consistent API error handling
PROJECT_RESPONSES = {
    status.HTTP_404_NOT_FOUND: {
        "model": HTTPErrorResponse,
        "description": "Project not found"
    },
    status.HTTP_409_CONFLICT: {
        "model": HTTPErrorResponse,
        "description": "Project name already exists"
    },
    status.HTTP_400_BAD_REQUEST: {
        "model": HTTPErrorResponse,
        "description": "Invalid project data"
    },
    status.HTTP_403_FORBIDDEN: {
        "model": HTTPErrorResponse,
        "description": "Operation not allowed or limit exceeded"
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": ValidationErrorResponse,
        "description": "Validation error (e.g., invalid data type, invalid enum value). For enum fields like 'state', ensure the value is one of the allowed options: 'PLANNED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED'."
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": HTTPErrorResponse,
        "description": "Internal server error"
    },
    status.HTTP_503_SERVICE_UNAVAILABLE: {
        "model": HTTPErrorResponse,
        "description": "Database service unavailable"
    }
}
