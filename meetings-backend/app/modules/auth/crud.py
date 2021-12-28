from typing import List

from sqlalchemy import select
from sqlmodel import Session, select

from app.modules.auth import security
from app.modules.auth.models import (
    PasswordUpdate,
    Role,
    RoleCreate,
    User,
    UserCreate,
    UserUpdate,
)


def select_all_users(session: Session) -> List[User]:
    return session.execute(select(User)).scalars().all()


def select_user_by_username(session: Session, username: str) -> User:
    return session.execute(select(User).where(User.username == username)).scalar_one()


def insert_user(session: Session, user: UserCreate) -> User:
    user_db = User(**user.dict(exclude={"plain_password": True, "roles": True}))
    # hash password and set roles
    user_db.password = security.hash_password(user.plain_password)
    for role in user.roles:
        role_db = session.get(Role, role.id)
        # if role doesn't exist, skip it
        if role_db is not None:
            user_db.roles.append(role_db)

    session.add(user_db)
    session.commit()

    return user_db


def update_user(session: Session, username: str, user_updated_data: UserUpdate) -> User:
    user = select_user_by_username(username)
    # go through all the fields defined an update them
    for k, v in user_updated_data.dict(exclude_unset=True).items():
        setattr(user, k, v)

    session.add(user)
    session.commit()

    return user


def update_password(
    session: Session, username: str, password_update: PasswordUpdate
) -> User:
    user = select_user_by_username(session, username)
    # first verify if the old password is correct
    if not security.verify_password(password_update.old_password, user.password):
        raise ValueError("Old password is not correct")
    # hash the new password and update it
    user.password = security.hash_password(password_update.new_password)

    session.add(user)
    session.commit()

    return user


def select_all_roles(session: Session) -> List[Role]:
    return session.execute(select(Role)).scalars().all()


def insert_role(session: Session, role: RoleCreate) -> Role:
    role_db = Role(**role.dict())
    session.add(role_db)
    session.commit()

    return role_db
