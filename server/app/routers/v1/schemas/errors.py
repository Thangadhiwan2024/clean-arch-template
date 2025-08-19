"""Schemas for error responses."""

from typing import List, Optional, Any, Dict
from pydantic import BaseModel


class ValidationErrorItem(BaseModel):
    """Schema for a single validation error item."""
    
    loc: List[str]
    msg: str
    type: str


class ValidationErrorResponse(BaseModel):
    """Schema for validation error responses."""
    
    detail: str
    errors: List[ValidationErrorItem]


class HTTPErrorResponse(BaseModel):
    """Base schema for HTTP error responses."""

    detail: str
    
    # Optional additional error data that can be included in some cases
    error_data: Optional[Dict[str, Any]] = None
