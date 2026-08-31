from fastapi import FastAPI
from sqlalchemy import text

from app.database.database import engine
from app.api.auth import router as auth_router 
from app.api.jobs import router as jobs_router
from app.api.job_eligibility import router as job_eligibility_router
from app.api.user_profile import router as user_profile_router
from app.api.bookmarks import router as bookmarks_router
from app.api.search import router as search_router
from app.api.job_syllabus import router as job_syllabus_router 
from app.api.job_exam_pattern import router as job_exam_pattern_router





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



app.include_router(
    job_eligibility_router,
    tags=["job Eligibility"]
)

app.include_router(
    user_profile_router,
)


app.include_router(
    bookmarks_router
)

app.include_router(
    search_router,
    prefix="/search",
    tags=["search"]
)
app.include_router(
    job_syllabus_router,
)

app.include_router(
    job_exam_pattern_router,
)