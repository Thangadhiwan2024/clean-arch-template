"""Mappers for project domain models, DTOs, and API schemas."""

from app.entities.models.project import Project
from app.use_cases.dto.project import ProjectDTO, ProjectListResponseDTO


class ProjectMapper:
    """Mapper between Project entities and DTOs."""

    @staticmethod
    def entity_to_dto(entity: Project) -> ProjectDTO:
        """Map a Project entity to a ProjectDTO."""
        return ProjectDTO(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            state=entity.state,
        )

    @staticmethod
    def create_list_response(
        total: int, skip: int, limit: int, entities: list[Project]
    ) -> ProjectListResponseDTO:
        """Create a ProjectListResponseDTO from project entities."""
        return ProjectListResponseDTO(
            total=total,
            skip=skip,
            limit=limit,
            items=[ProjectMapper.entity_to_dto(entity) for entity in entities],
        )
