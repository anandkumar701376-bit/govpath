from fastapi import FastAPI
from sqlalchemy import text

from app.database.database import engine
from app.api.auth import router as auth_router 
from app.api.jobs import router as jobs_router



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

@app.get("/db-test")
def database_test():
    with engine.connect() as connection:
        result=connection.execute(text("SELECT 1"))
        
        return{
            "database":"connected",
            "result":result.scalar()
        }
        
        

