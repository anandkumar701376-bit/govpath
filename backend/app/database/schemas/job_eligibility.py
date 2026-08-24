
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class JobEligibilityCreate(BaseModel):
    minimum_age: int | None = Field(default=None, ge=0)
    maximum_age: int | None = Field(default=None, ge=0)
    age_relaxation_available: bool = False

    education_level: str | None = Field(default=None, max_length=100)
    required_degree: str | None = Field(default=None, max_length=150)
    minimum_percentage: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    nationality: str | None = Field(default=None, max_length=100)

    experience_required: bool = False
    minimum_experience_years: float | None = Field(
        default=None,
        ge=0,
    )

    physical_standard_required: bool = False
    medical_fitness_required: bool = False

    gender_eligibility: str | None = Field(
        default=None,
        max_length=20,
    )

    eligibility_notes: str | None = None


class JobEligibilityUpdate(BaseModel):
    minimum_age: int | None = Field(default=None, ge=0)
    maximum_age: int | None = Field(default=None, ge=0)
    age_relaxation_available: bool | None = None

    education_level: str | None = Field(default=None, max_length=100)
    required_degree: str | None = Field(default=None, max_length=150)
    minimum_percentage: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    nationality: str | None = Field(default=None, max_length=100)

    experience_required: bool | None = None
    minimum_experience_years: float | None = Field(
        default=None,
        ge=0,
    )

    physical_standard_required: bool | None = None
    medical_fitness_required: bool | None = None

    gender_eligibility: str | None = Field(
        default=None,
        max_length=20,
    )

    eligibility_notes: str | None = None


class JobEligibilityRead(JobEligibilityCreate):
    id: UUID
    job_id: UUID
    created_at: datetime
    updated_at: datetime