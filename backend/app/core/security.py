import base64
import hashlib
import hmac
import os

from uuid import uuid4

from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import JWTError, jwt


load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not set")

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)


def hash_password(password: str, salt: bytes | None = None) -> str:

    salt_bytes = salt or os.urandom(16)

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt_bytes,
        120_000,
    )

    salt_b64 = base64.urlsafe_b64encode(salt_bytes).decode()
    digest_b64 = base64.urlsafe_b64encode(digest).decode()

    return f"{salt_b64}${digest_b64}"


def verify_password(password: str, stored_hash: str) -> bool:

    try:
        salt_b64, digest_b64 = stored_hash.split("$", 1)

        salt_bytes = base64.urlsafe_b64decode(
            salt_b64.encode()
        )

        expected_digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt_bytes,
            120_000,
        )

        return hmac.compare_digest(
            base64.urlsafe_b64decode(digest_b64.encode()),
            expected_digest,
        )

    except (ValueError, TypeError):
        return False
def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": user_id,
        "jti": str(uuid4()),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        user_id = payload.get("sub")

        if not user_id:
            return None

        return user_id

    except JWTError:
        return None


def decode_token_payload(token: str) -> dict | None:
    try:
        return jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )
    except JWTError:
        return None