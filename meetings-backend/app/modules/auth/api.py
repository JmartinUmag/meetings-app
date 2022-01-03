from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session

from app.database import get_db_session
from app.modules.auth.crud import (
    insert_role,
    insert_user,
    select_all_roles,
    select_all_users,
    select_user_by_username,
    update_password,
    update_user,
)
from app.modules.auth.models import (
    APIToken,
    PasswordUpdate,
    Role,
    RoleCreate,
    User,
    UserCreate,
    UserRead,
    UserUpdate,
)
from app.modules.auth.security import (
    RoleChecker,
    auth_exception,
    authenticate_user,
    create_jwt,
    get_current_active_user,
)

allow_manage_users = RoleChecker(["admin"])

router = APIRouter()


@router.get(
    "/users/", response_model=List[UserRead], dependencies=[Depends(allow_manage_users)]
)
async def get_users(session: Session = Depends(get_db_session)):
    return select_all_users(session)


@router.get("/users/me", response_model=UserRead)
async def get_user_me(
    user: User = Depends(get_current_active_user),
    session: Session = Depends(get_db_session),
):
    return select_user_by_username(session, user.username)


@router.get(
    "/users/{username}",
    response_model=UserRead,
    dependencies=[Depends(get_current_active_user)],
)
async def get_user(username: str, session: Session = Depends(get_db_session)):
    try:
        return select_user_by_username(session, username)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")


@router.post(
    "/users/", response_model=UserRead, dependencies=[Depends(allow_manage_users)]
)
async def create_user(user: UserCreate, session: Session = Depends(get_db_session)):
    try:
        return insert_user(session, user)
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="User already exists (by its username)"
        )


async def _modify_user(username: str, user_data: UserUpdate, session: Session) -> User:
    try:
        return update_user(session, username, user_data)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")


@router.patch("/users/me", response_model=UserRead)
async def modify_user_me(
    user_data: UserUpdate,
    user: User = Depends(get_current_active_user),
    session: Session = Depends(get_db_session),
):
    return _modify_user(user.username, user_data, session)


@router.patch(
    "/users/{username}",
    response_model=UserRead,
    dependencies=[Depends(allow_manage_users)],
)
async def modify_user(
    username: str, user_data: UserUpdate, session: Session = Depends(get_db_session)
):
    return _modify_user(username, user_data, session)


@router.post("/users/me/change-password", response_model=UserRead)
async def change_my_password(
    password_change: PasswordUpdate,
    user: User = Depends(get_current_active_user),
    session: Session = Depends(get_db_session),
):
    try:
        update_password(session, user.username, password_change)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/roles/",
    response_model=List[Role],
    dependencies=[Depends(get_current_active_user)],
)
async def get_roles(session: Session = Depends(get_db_session)):
    return select_all_roles(session)


@router.post(
    "/roles/", response_model=Role, dependencies=[Depends(get_current_active_user)]
)
async def create_role(role: RoleCreate, session: Session = Depends(get_db_session)):
    try:
        return insert_role(session, role)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Role already exists")


@router.post("/token", response_model=APIToken)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise auth_exception("Wrong username or password")
    access_token = create_jwt(data={"sub": user.username, "name": user.fullname})
    return APIToken(access_token=access_token, token_type="bearer")
