import datetime as dt
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import select

from app.config import settings
from app.database import engine
from app.modules.auth.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(username: str) -> Optional[User]:
    """
    Get user from database by username
    """
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        user = await session.execute(select(User).where(User.username == username))
        return user.scalars().first()


async def authenticate_user(username: str, password: str) -> Optional[User]:
    """
    Authenticate user and return user if successful
    """
    user = await get_user(username)
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


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
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

    user = await get_user(username)
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Validate if the user is active (return exception if not)
    """
    if not current_user.enabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def auth_exception(detail: str) -> Exception:
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
