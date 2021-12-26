import datetime as dt
from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, Column, String, DateTime

if TYPE_CHECKING:
    from app.modules.auth.models import User


class MeetingUserLink(SQLModel, table=True):
    __tablename__ = "meetings_users"

    meeting_id: int = Field(default=None, primary_key=True, foreign_key="meetings.id")
    user_id: int = Field(default=None, primary_key=True, foreign_key="users.id")


class Meeting(SQLModel, table=True):
    __tablename__ = "meetings"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(String(length=64)))
    summary: str = Field(sa_column=Column(String(length=128)))
    datetime: dt.datetime = Field(sa_column=Column(DateTime))
    place: str = Field(sa_column=Column(String(length=128)))

    assistants: List["User"] = Relationship(
        back_populates="meetings", link_model=MeetingUserLink
    )
    files: List["File"] = Relationship(back_populates="meetings")


class TaskBase(SQLModel):
    text: str = Field(sa_column=Column(String(length=128)))
    user_id: int = Field(foreign_key="users.id")


class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: dt.datetime = Field(sa_column=Column(DateTime))

    user: "User" = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    pass


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(length=16)))


class File(SQLModel, table=True):
    __tablename__ = "files"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(length=255)))
    path: str = Field(sa_column=Column(String(length=255)))
    meeting_id: int = Field(foreign_key="meetings.id")

    meeting: "Meeting" = Relationship(back_populates="files")
