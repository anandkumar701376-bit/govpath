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


class JobEligibility(Base):
    __tablename__ = "job_eligibility"

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

    minimum_age: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    maximum_age: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    age_relaxation_available: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    education_level: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    required_degree: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    minimum_percentage: Mapped[float | None] = mapped_column(
        DECIMAL(5, 2),
        nullable=True,
    )

    nationality: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    experience_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    minimum_experience_years: Mapped[float | None] = mapped_column(
        DECIMAL(3, 1),
        nullable=True,
    )

    physical_standard_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    medical_fitness_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    gender_eligibility: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    eligibility_notes: Mapped[str | None] = mapped_column(
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
        back_populates="eligibility",
    )