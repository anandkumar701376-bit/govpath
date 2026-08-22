import uuid
from datetime import date, datetime


from sqlalchemy import Boolean, Date, DateTime, DECIMAL, Integer, String, Text,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base

from sqlalchemy.dialects.postgresql import UUID
class Job(Base):
    __tablename__ = 'jobs'

    id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid.uuid4,
)
    
    job_title: Mapped[str] = mapped_column(String(200), nullable=False)
    job_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    organization: Mapped[str | None] = mapped_column(String(150), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sub_category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    application_mode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    application_start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    application_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    exam_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    application_fee: Mapped[float | None] = mapped_column(DECIMAL(10, 2), nullable=True)
    official_notification_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    official_apply_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    official_website: Mapped[str | None] = mapped_column(Text, nullable=True)
    job_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class JobEligibility(Base):
    __tablename__ = 'job_eligibility'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("jobs.id"),nullable=False)
    minimum_age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    maximum_age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    age_relaxation_available: Mapped[bool] = mapped_column(Boolean, default=False)
    education_level: Mapped[str | None] = mapped_column(String(100), nullable=True)
    required_degree: Mapped[str | None] = mapped_column(String(150), nullable=True)
    minimum_percentage: Mapped[float | None] = mapped_column(DECIMAL(5, 2), nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(100), nullable=True)
    experience_required: Mapped[bool] = mapped_column(Boolean, default=False)
    minimum_experience_years: Mapped[float | None] = mapped_column(DECIMAL(3, 1), nullable=True)
    physical_standard_required: Mapped[bool] = mapped_column(Boolean, default=False)
    medical_fitness_required: Mapped[bool] = mapped_column(Boolean, default=False)
    gender_eligibility: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eligibility_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
