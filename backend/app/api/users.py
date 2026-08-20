from fastapi import APIRouter, HTTPException

from app.services.user_service import UserService

router = APIRouter()


@router.get("/")
def list_users():
    return UserService.list_users()


@router.get("/{user_id}")
def get_user(user_id: str):
    user = UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
