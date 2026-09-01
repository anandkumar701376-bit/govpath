from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field


class StudyTaskCreate(BaseModel):
    roadmap_id: UUID | None = None
    roadmap_stage_id: UUID | None = None
    user_id: UUID
    job_id: UUID | None = None

    task_title: str
    task_description: str | None = None
    task_type: str | None = None

    subject: str | None = None
    topic: str | None = None

    priority: str | None = None

    estimated_duration_minutes: int | None = Field(
        default=None,
        ge=0,
    )

    due_date: date | None = None
    status: str | None = None

    completion_percentage: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    ai_generated: bool = False
    resource_id: UUID | None = None
    notes: str | None = None


class StudyTaskUpdate(BaseModel):
    roadmap_id: UUID | None = None
    roadmap_stage_id: UUID | None = None
    job_id: UUID | None = None

    task_title: str | None = None
    task_description: str | None = None
    task_type: str | None = None

    subject: str | None = None
    topic: str | None = None

    priority: str | None = None

    estimated_duration_minutes: int | None = Field(
        default=None,
        ge=0,
    )

    due_date: date | None = None
    status: str | None = None

    completion_percentage: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    ai_generated: bool | None = None
    resource_id: UUID | None = None
    notes: str | None = None


class StudyTaskRead(BaseModel):
    id: UUID

    roadmap_id: UUID | None
    roadmap_stage_id: UUID | None
    user_id: UUID
    job_id: UUID | None

    task_title: str
    task_description: str | None
    task_type: str | None

    subject: str | None
    topic: str | None

    priority: str | None
    estimated_duration_minutes: int | None

    due_date: date | None
    status: str | None
    completion_percentage: float | None

    ai_generated: bool
    resource_id: UUID | None
    notes: str | None

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }