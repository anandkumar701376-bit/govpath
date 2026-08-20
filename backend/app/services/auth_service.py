from datetime import datetime

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.database.models.user import User


class AuthService:

    @staticmethod
    def register_user(
        db: Session,
        full_name: str,
        email: str,
        password: str,
        mobile_number: str | None = None,
    ) -> User:

        email = email.lower()

        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            raise ValueError("Email already registered")

        user = User(
            full_name=full_name,
            email=email,
            mobile_number=mobile_number,
            password_hash=hash_password(password),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def login_user(
        db: Session,
        email: str,
        password: str,
    ) -> str:

        email = email.lower()

        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if not user:
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("User account is inactive")

        if not verify_password(
            password,
            user.password_hash
        ):
            raise ValueError("Invalid email or password")

        user.last_login = datetime.utcnow()

        db.commit()

        token = create_access_token(str(user.id))

        return token