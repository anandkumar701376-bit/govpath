from datetime import date
from typing import Optional


from uuid import UUID
from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    job_title: str= Field(..., min_length=2, max_length=200)
    job_code: str = Field(..., min_length=2, max_length=50)
    organization: Optional[str] = Field(None, max_length=150)
    category: Optional[str] = Field(None, max_length=100)
    sub_category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    application_mode: Optional[str] = Field(None, max_length=20)
    application_start_date: Optional[date] = None
    application_end_date: Optional[date] = None
    exam_date: Optional[date] = None
    application_fee: Optional[float] = None
    official_notification_url: Optional[str] = None
    official_apply_url: Optional[str] = None
    official_website: Optional[str] = None
    job_status: Optional[str] = Field(None, max_length=20)
    is_featured: bool = False


class JobRead(JobCreate):
    id: UUID




class JobUpdate(BaseModel):
    job_title: Optional[str] = Field(None, min_length=2, max_length=200)
    job_code: Optional[str] = Field(None, min_length=2, max_length=50)
    organization: Optional[str] = Field(None, max_length=150)
    category: Optional[str] = Field(None, max_length=100)
    sub_category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    application_mode: Optional[str] = Field(None, max_length=20)
    application_start_date: Optional[date] = None
    application_end_date: Optional[date] = None
    exam_date: Optional[date] = None
    application_fee: Optional[float] = None
    official_notification_url: Optional[str] = None
    official_apply_url: Optional[str] = None
    official_website: Optional[str] = None
    job_status: Optional[str] = Field(None, max_length=20)
    is_featured: Optional[bool] = None