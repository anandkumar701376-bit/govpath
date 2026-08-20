from datetime import datetime

from sqlalchemy import Boolean, DateTime, DECIMAL, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class MockTest(Base):
    __tablename__ = 'mock_tests'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    job_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    test_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    total_questions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_marks: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    negative_marking: Mapped[bool] = mapped_column(Boolean, default=False)
    negative_marks: Mapped[float | None] = mapped_column(DECIMAL(3, 2), nullable=True)
    passing_marks: Mapped[int | None] = mapped_column(Integer, nullable=True)
    difficulty_level: Mapped[str | None] = mapped_column(String(20), nullable=True)
    language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_free: Mapped[bool] = mapped_column(Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
