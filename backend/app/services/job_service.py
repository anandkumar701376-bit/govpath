from datetime import datetime
from typing import Any

JOBS: dict[str, dict[str, Any]] = {}


class JobService:
    @staticmethod
    def list_jobs() -> list[dict[str, Any]]:
        return list(JOBS.values())

    @staticmethod
    def get_job(job_id: str) -> dict[str, Any] | None:
        return JOBS.get(job_id)

    @staticmethod
    def create_job(payload: dict[str, Any]) -> dict[str, Any]:
        job_id = payload.get("id") or f"job-{len(JOBS) + 1:04d}"
        job = {**payload, "id": job_id, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()}
        JOBS[job_id] = job
        return job
