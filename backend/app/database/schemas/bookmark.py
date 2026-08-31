from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BookmarkRead(BaseModel):
    id: UUID
    user_id: UUID
    job_id: UUID
    created_at: datetime