from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field


class UserProfileCreate(BaseModel):
    profile_photo: str | None = Field(default=None, max_length=500)
    bio: str | None = None
    contact_email: str | None = Field(default=None, max_length=255)

    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=20)
    nationality: str | None = Field(default=None, max_length=100)
    category: str | None = Field(default=None, max_length=20)

    state: str | None = Field(default=None, max_length=100)
    district: str | None = Field(default=None, max_length=100)

    education_level: str | None = Field(default=None, max_length=100)
    degree: str | None = Field(default=None, max_length=150)
    percentage: float | None = Field(default=None, ge=0, le=100)
    graduation_year: int | None = Field(default=None, ge=1900)

    experience_years: float | None = Field(default=None, ge=0)


class UserProfileUpdate(BaseModel):
    profile_photo: str | None = Field(default=None, max_length=500)
    bio: str | None = None
    contact_email: str | None = Field(default=None, max_length=255)

    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=20)
    nationality: str | None = Field(default=None, max_length=100)
    category: str | None = Field(default=None, max_length=20)

    state: str | None = Field(default=None, max_length=100)
    district: str | None = Field(default=None, max_length=100)

    education_level: str | None = Field(default=None, max_length=100)
    degree: str | None = Field(default=None, max_length=150)
    percentage: float | None = Field(default=None, ge=0, le=100)
    graduation_year: int | None = Field(default=None, ge=1900)

    experience_years: float | None = Field(default=None, ge=0)


class UserProfileRead(UserProfileCreate):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime