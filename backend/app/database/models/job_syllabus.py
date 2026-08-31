import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    DECIMAL,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class JobSyllabus(Base):
    __tablename__ = "job_syllabus"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id"),
        nullable=False,
        index=True,
    )

    exam_pattern_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("job_exam_pattern.id"),
        nullable=False,
        index=True,
    )

    stage_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    subject_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    topic_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    sub_topic_name: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    difficulty_level: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    weightage: Mapped[float | None] = mapped_column(
        DECIMAL(5, 2),
        nullable=True,
    )

    is_mandatory: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    reference_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    job = relationship(
        "Job",
        back_populates="syllabus",
    )

    exam_pattern = relationship(
        "JobExamPattern",
        back_populates="syllabus",
    )