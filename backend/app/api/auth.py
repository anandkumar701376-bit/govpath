from fastapi import APIRouter, Depends, HTTPException, status 
from datetime import datetime
from sqlalchemy.orm import Session

from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer

from app.database.models.user import User
from app.database.schemas.auth import TokenPayload, UserLogin, UserOut, UserRegister
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.services.auth_service import AuthService

from app.core.security import decode_token_payload
from app.database.models.revoked_token import RevokedToken
router = APIRouter()
security = HTTPBearer()

@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: UserRegister,
    db: Session = Depends(get_db),
):
    try:
        user = AuthService.register_user(
            db=db,
            full_name=payload.full_name,
            email=payload.email,
            password=payload.password,
            mobile_number=payload.mobile_number,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return {
        "id": str(user.id),
        "full_name": user.full_name,
        "email": user.email,
        "mobile_number": user.mobile_number,
        "created_at": user.created_at,
    }


@router.post("/login", response_model=TokenPayload)
def login(
    payload: UserLogin,
    db: Session = Depends(get_db),
):
    try:
        token = AuthService.login_user(
            db=db,
            email=payload.email,
            password=payload.password,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    return {
        "access_token": token,
        "token_type": "bearer",
    }

@router.get("/me", response_model=UserOut)
def me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": str(current_user.id),
        "full_name": current_user.full_name,
        "email": current_user.email,
        "mobile_number": current_user.mobile_number,
        "created_at": current_user.created_at,
    }


@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    payload = decode_token_payload(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    jti = payload.get("jti")
    exp = payload.get("exp")

    if not user_id or not jti or not exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    existing_token = (
        db.query(RevokedToken)
        .filter(RevokedToken.jti == jti)
        .first()
    )

    if existing_token:
        return {"message": "Already logged out"}

    revoked_token = RevokedToken(
        jti=jti,
        user_id=user_id,
        expires_at=datetime.fromtimestamp(exp),
    )

    db.add(revoked_token)
    db.commit()

    return {"message": "Logged out successfully"}