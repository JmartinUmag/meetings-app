import datetime as dt
from typing import List, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import engine
from app.modules.auth import crud as auth_crud
from app.modules.auth.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str) -> Optional[User]:
    """
    Get user from database by username
    """
    try:
        session = sessionmaker(engine, expire_on_commit=False)
        with session() as session:
            return auth_crud.select_user_by_username(
                session, username, include_roles=True
            )
    except NoResultFound:
        return None


def authenticate_user(username: str, password: str) -> Optional[User]:
    """
    Authenticate user and return user if successful
    """
    user = get_user(username)
    if user is None or not verify_password(password, user.password):
        return None

    return user


def create_jwt(data: dict, expires_delta: dt.timedelta = dt.timedelta(hours=1)) -> str:
    """
    Creates JWT token with given data and expiration time
    """
    to_encode = {
        **data,
        "iat": dt.datetime.utcnow(),
        "exp": dt.datetime.utcnow() + expires_delta,
    }

    encoded_jwt = jwt.encode(to_encode, key=settings.secret_key, algorithm="HS256")

    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Decode the JWT and return the corresponding user
    """
    credentials_exception = auth_exception("Could not validate credentials")

    try:
        payload = jwt.decode(token, key=settings.secret_key, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(username)

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Validate if user is active
    """
    if not current_user.enabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def auth_exception(detail: str) -> Exception:
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_active_user)):
        if not any(r.name in self.allowed_roles for r in user.roles):
            raise HTTPException(status_code=403, detail="Operation not permitted")
