"""SQLite models for projects."""

import uuid
from datetime import UTC, datetime
from typing import Optional

from sqlalchemy import String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.entities.models.project import ProjectState
from app.infrastructures.sqlite_db.database import Base


class ProjectModel(Base):
    """SQLite model for projects."""

    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    state: Mapped[ProjectState] = mapped_column(
        Enum(ProjectState), default=ProjectState.PLANNED, nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC), onupdate=datetime.now(UTC))
