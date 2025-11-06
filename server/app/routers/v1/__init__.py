"""v1 routers for Project Management service."""

from fastapi import APIRouter


from app.routers.v1.endpoints.project import project_router

router = APIRouter(prefix="/v1")

router.include_router(project_router)
