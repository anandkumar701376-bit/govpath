from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class JobSyllabusCreate(BaseModel):
    exam_pattern_id: UUID
    stage_name: str
    subject_name: str
    topic_name: str
    sub_topic_name: str | None = None
    difficulty_level: str | None = None
    weightage: float | None = None
    is_mandatory: bool = True
    reference_notes: str | None = None


class JobSyllabusUpdate(BaseModel):
    exam_pattern_id: UUID | None = None
    stage_name: str | None = None
    subject_name: str | None = None
    topic_name: str | None = None
    sub_topic_name: str | None = None
    difficulty_level: str | None = None
    weightage: float | None = None
    is_mandatory: bool | None = None
    reference_notes: str | None = None


class JobSyllabusRead(BaseModel):
    id: UUID
    job_id: UUID
    exam_pattern_id: UUID
    stage_name: str
    subject_name: str
    topic_name: str
    sub_topic_name: str | None
    difficulty_level: str | None
    weightage: float | None
    is_mandatory: bool
    reference_notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }