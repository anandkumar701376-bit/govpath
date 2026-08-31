import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, DECIMAL, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    job_title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    job_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    organization: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    sub_category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    application_mode: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    application_start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    application_end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    exam_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    application_fee: Mapped[float | None] = mapped_column(
        DECIMAL(10, 2),
        nullable=True,
    )

    official_notification_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    official_apply_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    official_website: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    job_status: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    is_featured: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
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

    eligibility = relationship(
        "JobEligibility",
        back_populates="job",
        uselist=False,
        cascade="all, delete-orphan",
    )
    
    bookmarks = relationship(
    "Bookmark",
    back_populates="job",
    cascade="all, delete-orphan",
)