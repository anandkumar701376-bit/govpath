from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SubjectCreate(BaseModel):
    subject_name: str
    subject_code: str
    category: str | None = None
    description: str | None = None
    icon_url: str | None = None
    is_active: bool = True


class SubjectUpdate(BaseModel):
    subject_name: str | None = None
    subject_code: str | None = None
    category: str | None = None
    description: str | None = None
    icon_url: str | None = None
    is_active: bool | None = None


class SubjectRead(BaseModel):
    id: UUID
    subject_name: str
    subject_code: str
    category: str | None
    description: str | None
    icon_url: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }