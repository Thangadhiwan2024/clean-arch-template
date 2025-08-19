"""SQLite implementation of the project repository."""

from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound, IntegrityError

from app.entities.errors.project import ProjectNotFoundError, ProjectNameExistsError
from app.entities.models.project import Project, ProjectState
from app.entities.repositories.project import ProjectRepositoryInterface
from app.infrastructures.sqlite_db.database import async_session
from app.infrastructures.sqlite_db.models.project import ProjectModel


class SQLiteProjectRepository(ProjectRepositoryInterface):
    """SQLite implementation of the project repository."""

    async def create_project(self, name: str, description: Optional[str] = None,
                             state: ProjectState = ProjectState.PLANNED) -> Project:
        """Create a new project with the provided details."""
        async with async_session() as session:
            try:
                # Create new project
                project_model = ProjectModel(name=name, description=description, state=state)
                session.add(project_model)
                await session.commit()
                await session.refresh(project_model)

                # Convert to entity
                return Project(
                    id=project_model.id,
                    name=project_model.name,
                    description=project_model.description,
                    state=project_model.state,
                )
            except IntegrityError:
                await session.rollback()
                raise ProjectNameExistsError(name)

    async def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """Retrieve a project by its ID."""
        async with async_session() as session:
            try:
                query = select(ProjectModel).where(ProjectModel.id == project_id)
                result = await session.execute(query)
                project_model = result.scalar_one()

                # Convert to entity
                return Project(
                    id=project_model.id,
                    name=project_model.name,
                    description=project_model.description,
                    state=project_model.state,
                )
            except NoResultFound:
                # Return None instead of raising an exception
                # The service layer will handle this by raising ProjectNotFoundError
                return None

    async def get_projects(self, skip: int = 0, limit: int = 100,
                           state: Optional[ProjectState] = None) -> List[Project]:
        """Retrieve projects with pagination and optional filtering by state."""
        async with async_session() as session:
            query = select(ProjectModel).offset(skip).limit(limit)
            
            # Apply state filter if provided
            if state is not None:
                query = query.where(ProjectModel.state == state)
                
            # Order by creation time (newest first)
            query = query.order_by(ProjectModel.created_at.desc())
            
            result = await session.execute(query)
            project_models = result.scalars().all()

            # Convert to entities
            return [
                Project(
                    id=model.id,
                    name=model.name,
                    description=model.description,
                    state=model.state,
                )
                for model in project_models
            ]

    async def update_project(self, project_id: str, name: Optional[str] = None,
                             description: Optional[str] = None,
                             state: Optional[ProjectState] = None) -> Optional[Project]:
        """Update an existing project with the provided data."""
        async with async_session() as session:
            try:
                # Find the project
                query = select(ProjectModel).where(ProjectModel.id == project_id)
                result = await session.execute(query)
                project_model = result.scalar_one()

                # Update fields if provided
                if name is not None:
                    project_model.name = name
                if description is not None:
                    project_model.description = description
                if state is not None:
                    project_model.state = state

                # Save changes
                await session.commit()
                await session.refresh(project_model)

                # Convert to entity
                return Project(
                    id=project_model.id,
                    name=project_model.name,
                    description=project_model.description,
                    state=project_model.state,
                )
            except NoResultFound:
                return None
            except IntegrityError:
                await session.rollback()
                if name:
                    raise ProjectNameExistsError(name)
                raise

    async def delete_project(self, project_id: str) -> bool:
        """Delete a project by its ID. Returns True if successful, False otherwise."""
        async with async_session() as session:
            try:
                # Find the project
                query = select(ProjectModel).where(ProjectModel.id == project_id)
                result = await session.execute(query)
                project_model = result.scalar_one()

                # Delete the project
                await session.delete(project_model)
                await session.commit()
                return True
            except NoResultFound:
                # Return False instead of raising an exception
                # The service layer will handle this by raising ProjectNotFoundError
                return False

    async def count_projects(self, state: Optional[ProjectState] = None) -> int:
        """Count the total number of projects, with optional filtering by state."""
        async with async_session() as session:
            query = select(func.count()).select_from(ProjectModel)
            
            # Apply state filter if provided
            if state is not None:
                query = query.where(ProjectModel.state == state)
                
            result = await session.execute(query)
            return result.scalar_one()
