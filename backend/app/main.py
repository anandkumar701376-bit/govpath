from fastapi import FastAPI
from sqlalchemy import text

from app.database.database import engine
from app.api.auth import router as auth_router 
from app.api.jobs import router as jobs_router
from app.api.job_eligibility import router as job_eligibility_router


app= FastAPI()


app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)



app.include_router(
    jobs_router,
    prefix="/jobs",
    tags=["Jobs"],
)



app.include_router(job_eligibility_router,tags=["job Eligibility"])



