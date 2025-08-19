"""API schemas for project endpoints."""

from typing import Optional, List

from pydantic import BaseModel, Field

from app.entities.models.project import ProjectState
from app.routers.v1.schemas.base import BaseSchema


class ProjectBase(BaseModel):
    """Base schema for project data."""

    name: str = Field(..., example="New Website Development")
    description: Optional[str] = Field(None, example="Website development for client XYZ")
    state: ProjectState = Field(default=ProjectState.PLANNED, example=ProjectState.PLANNED)


class ProjectCreateRequest(ProjectBase):
    """Request schema for project creation."""

    pass


class ProjectUpdateRequest(BaseModel):
    """Request schema for project update."""

    name: Optional[str] = Field(None, example="Updated Website Development")
    description: Optional[str] = Field(None, example="Updated description")
    state: Optional[ProjectState] = Field(None, example=ProjectState.IN_PROGRESS)


class ProjectResponse(ProjectBase):
    """Response schema for project data."""

    id: str = Field(..., example="a1b2c3d4e5f6")
    
    class Config:
        """Config for the schema."""

        from_attributes = True


class ProjectListRequest(BaseModel):
    """Request schema for project listing."""

    skip: int = Field(0, ge=0, example=0)
    limit: int = Field(100, ge=1, le=1000, example=100)
    state: Optional[ProjectState] = Field(None, example=ProjectState.IN_PROGRESS)


class ProjectListResponse(BaseSchema):
    """Response schema for project listing."""

    total: int = Field(..., example=100)
    skip: int = Field(..., example=0)
    limit: int = Field(..., example=100)
    items: List[ProjectResponse] = Field(..., example=[])
