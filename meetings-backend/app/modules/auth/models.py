from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Column, Field, Relationship, SQLModel, String

from app.modules.meetings.models import MeetingUserLink

if TYPE_CHECKING:
    from app.modules.meetings.models import Meeting, Task


class UserRoleLink(SQLModel, table=True):
    __tablename__ = "users_roles"

    user_id: int = Field(primary_key=True, foreign_key="users.id")
    role_id: int = Field(primary_key=True, foreign_key="roles.id")


class RoleBase(SQLModel):
    name: str = Field(sa_column=Column(String(32), index=True, unique=True))


class Role(RoleBase, table=True):
    __tablename__ = "roles"

    id: int = Field(primary_key=True, nullable=False)

    users: List["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)


class RoleCreate(RoleBase):
    pass


class UserBase(SQLModel):
    username: str = Field(sa_column=Column(String(32), index=True, unique=True))
    fullname: str = Field(sa_column=Column(String(64)))


class UserExtra(UserBase):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    enabled: bool = Field(default=True)


class User(UserExtra, table=True):
    __tablename__ = "users"

    password: str = Field(sa_column=Column(String(128)))

    meetings: List["Meeting"] = Relationship(
        back_populates="assistants", link_model=MeetingUserLink
    )
    tasks: List["Task"] = Relationship(back_populates="assignee")
    roles: List["Role"] = Relationship(back_populates="users", link_model=UserRoleLink)


class UserRead(UserExtra):
    roles: List["Role"] = Field(default=[])


class UserCreate(UserBase):
    plain_password: str = Field(max_length=64)
    roles: List[str] = []


class UserUpdate(SQLModel):
    username: Optional[str] = Field(default=None)
    fullname: Optional[str] = Field(default=None)
    enabled: Optional[bool] = Field(default=None)
    roles: Optional[List[str]] = Field(default=None)


class PasswordUpdate(SQLModel):
    old_password: str = Field(max_length=64)
    new_password: str = Field(max_length=64)


class APIToken(SQLModel):
    access_token: str
    token_type: str
