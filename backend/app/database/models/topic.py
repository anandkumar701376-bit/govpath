import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, DECIMAL, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    topic_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    topic_code: Mapped[str | None] = mapped_column(
        String(30),
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

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
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