from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TopicCreate(BaseModel):
    subject_id: UUID
    topic_name: str
    topic_code: str | None = None
    difficulty_level: str | None = None
    weightage: float | None = None
    description: str | None = None
    is_active: bool = True


class TopicUpdate(BaseModel):
    subject_id: UUID | None = None
    topic_name: str | None = None
    topic_code: str | None = None
    difficulty_level: str | None = None
    weightage: float | None = None
    description: str | None = None
    is_active: bool | None = None


class TopicRead(BaseModel):
    id: UUID
    subject_id: UUID
    topic_name: str
    topic_code: str | None
    difficulty_level: str | None
    weightage: float | None
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }