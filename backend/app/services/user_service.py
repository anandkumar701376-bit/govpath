from datetime import datetime
from typing import Any

from app.services.auth_service import USERS


class UserService:
    @staticmethod
    def list_users() -> list[dict[str, Any]]:
        return list(USERS.values())

    @staticmethod
    def get_user(user_id: str) -> dict[str, Any] | None:
        return USERS.get(user_id)

    @staticmethod
    def update_user(user_id: str, **kwargs) -> dict[str, Any] | None:
        user = USERS.get(user_id)
        if not user:
            return None
        user.update(kwargs)
        user["updated_at"] = datetime.utcnow()
        return user
