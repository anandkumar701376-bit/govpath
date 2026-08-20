from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.auth import get_current_user

router = APIRouter()


@router.get("/")
def get_profile(current_user: dict = Depends(get_current_user)):
    return current_user


@router.put("/")
def update_profile(payload: dict, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return {"message": "Profile updated", "data": payload}
