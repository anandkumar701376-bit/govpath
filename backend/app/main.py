from fastapi import FastAPI
from sqlalchemy import text

from app.database.database import engine
from app.api.auth import router as auth_router 


app= FastAPI()
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

@app.get("/db-test")
def database_test():
    with engine.connect() as connection:
        result=connection.execute(text("SELECT 1"))
        
        return{
            "database":"connected",
            "result":result.scalar
        }