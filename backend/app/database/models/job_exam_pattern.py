import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    DECIMAL,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class JobExamPattern(Base):
    __tablename__ = "job_exam_pattern"

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

    stage_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    stage_order: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    exam_mode: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    exam_type: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    subject_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    questions: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    marks: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    duration_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    negative_marking: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    negative_marks: Mapped[float | None] = mapped_column(
        DECIMAL(3, 2),
        nullable=True,
    )

    qualifying_marks: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    language: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    remarks: Mapped[str | None] = mapped_column(
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
        back_populates="exam_patterns",
    )

    syllabus = relationship(
        "JobSyllabus",
        back_populates="exam_pattern",
        cascade="all, delete-orphan",
    )