from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, DECIMAL, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Subject(Base):
    __tablename__ = 'subjects'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    subject_name: Mapped[str] = mapped_column(String(100), nullable=False)
    subject_code: Mapped[str] = mapped_column(String(20), nullable=False)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Topic(Base):
    __tablename__ = 'topics'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    subject_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    topic_name: Mapped[str] = mapped_column(String(150), nullable=False)
    topic_code: Mapped[str | None] = mapped_column(String(30), nullable=True)
    difficulty_level: Mapped[str | None] = mapped_column(String(20), nullable=True)
    weightage: Mapped[float | None] = mapped_column(DECIMAL(5, 2), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Roadmap(Base):
    __tablename__ = 'roadmaps'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    job_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    roadmap_title: Mapped[str] = mapped_column(String(200), nullable=False)
    roadmap_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    target_exam_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    total_duration_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_stages: Mapped[int | None] = mapped_column(Integer, nullable=True)
    completion_percentage: Mapped[float | None] = mapped_column(DECIMAL(5, 2), nullable=True)
    status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    ai_generated: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class RoadmapStage(Base):
    __tablename__ = 'roadmap_stages'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    roadmap_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    stage_name: Mapped[str] = mapped_column(String(100), nullable=False)
    stage_order: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    estimated_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    completion_percentage: Mapped[float | None] = mapped_column(DECIMAL(5, 2), nullable=True)
    status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    ai_focus_area: Mapped[str | None] = mapped_column(String(100), nullable=True)
    target_hours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class StudyTask(Base):
    __tablename__ = 'study_tasks'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    roadmap_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    roadmap_stage_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    job_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    task_title: Mapped[str] = mapped_column(String(200), nullable=False)
    task_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    task_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    subject: Mapped[str | None] = mapped_column(String(100), nullable=True)
    topic: Mapped[str | None] = mapped_column(String(150), nullable=True)
    priority: Mapped[str | None] = mapped_column(String(20), nullable=True)
    estimated_duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    completion_percentage: Mapped[float | None] = mapped_column(DECIMAL(5, 2), nullable=True)
    ai_generated: Mapped[bool] = mapped_column(Boolean, default=False)
    resource_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LearningResource(Base):
    __tablename__ = 'learning_resources'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    job_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    subject_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    topic_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    resource_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    author: Mapped[str | None] = mapped_column(String(150), nullable=True)
    publisher: Mapped[str | None] = mapped_column(String(150), nullable=True)
    language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)
    thumbnail_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty_level: Mapped[str | None] = mapped_column(String(20), nullable=True)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rating: Mapped[float | None] = mapped_column(DECIMAL(3, 2), nullable=True)
    is_free: Mapped[bool] = mapped_column(Boolean, default=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
