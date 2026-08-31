from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class JobExamPatternCreate(BaseModel):
    stage_name: str
    stage_order: int | None = None
    exam_mode: str | None = None
    exam_type: str | None = None
    subject_name: str | None = None
    questions: int | None = None
    marks: int | None = None
    duration_minutes: int | None = None
    negative_marking: bool = False
    negative_marks: float | None = None
    qualifying_marks: int | None = None
    language: str | None = None
    remarks: str | None = None


class JobExamPatternUpdate(BaseModel):
    stage_name: str | None = None
    stage_order: int | None = None
    exam_mode: str | None = None
    exam_type: str | None = None
    subject_name: str | None = None
    questions: int | None = None
    marks: int | None = None
    duration_minutes: int | None = None
    negative_marking: bool | None = None
    negative_marks: float | None = None
    qualifying_marks: int | None = None
    language: str | None = None
    remarks: str | None = None


class JobExamPatternRead(BaseModel):
    id: UUID
    job_id: UUID
    stage_name: str
    stage_order: int | None
    exam_mode: str | None
    exam_type: str | None
    subject_name: str | None
    questions: int | None
    marks: int | None
    duration_minutes: int | None
    negative_marking: bool
    negative_marks: float | None
    qualifying_marks: int | None
    language: str | None
    remarks: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }