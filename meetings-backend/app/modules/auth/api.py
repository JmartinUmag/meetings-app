from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.modules.auth.models import APIToken, User, UserRead
from app.modules.auth.security import (
    auth_exception,
    authenticate_user,
    create_jwt,
    hash_password,
)

router = APIRouter()


@router.get("/users/", response_model=List[UserRead])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/users/{username}", response_model=User)
async def create_user(username: str, session: AsyncSession = Depends(get_session)):
    user = await session.execute(select(User).where(User.username == username))
    return user.scalars().first()


@router.post("/users/", response_model=User)
async def create_user(user: User, session: AsyncSession = Depends(get_session)):
    user.password = hash_password(user.password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.post("/token", response_model=APIToken)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if user is None:
        return auth_exception("Usuario o contraseña incorrecta")
    access_token = create_jwt(data={"sub": user.username, "name": user.fullname})
    return APIToken(access_token=access_token, token_type="bearer")
