"""Services for Project Management Service."""

from functools import lru_cache

from app.entities.repositories.project import ProjectRepositoryInterface
from app.infrastructures.sqlite_db.project import SQLiteProjectRepository
from app.use_cases.project import ProjectService


def get_project_repository() -> ProjectRepositoryInterface:
    """Get the project repository."""
    return SQLiteProjectRepository()


@lru_cache
def get_project_service() -> ProjectService:
    """Get the Project Service."""
    project_repository = get_project_repository()
    return ProjectService(project_repository=project_repository)
