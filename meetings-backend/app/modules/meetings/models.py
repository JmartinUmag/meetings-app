import datetime as dt
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, String

if TYPE_CHECKING:
    from app.modules.auth.models import User


class MeetingUserLink(SQLModel, table=True):
    __tablename__ = "meetings_users"

    meeting_id: int = Field(primary_key=True, foreign_key="meetings.id")
    user_id: int = Field(primary_key=True, foreign_key="users.id")


class MeetingBase(SQLModel):
    title: str = Field(sa_column=Column(String(length=64)))
    summary: str = Field(sa_column=Column(String(length=128)))
    datetime: dt.datetime = Field(sa_column=Column(DateTime))
    place: str = Field(sa_column=Column(String(length=128)))


class Meeting(MeetingBase, table=True):
    __tablename__ = "meetings"

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)

    assistants: List["User"] = Relationship(
        back_populates="meetings", link_model=MeetingUserLink
    )
    files: List["File"] = Relationship(back_populates="meeting")


class MeetingCreate(MeetingBase):
    assistants_ids: List[int] = Field(default=[])


class MeetingRead(MeetingBase):
    assistants: List["User"] = []
    files: List["File"] = []


class TaskBase(SQLModel):
    text: str = Field(sa_column=Column(String(length=128)))
    asignee_id: int = Field(foreign_key="users.id")


class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    created_at: dt.datetime = Field(sa_column=Column(DateTime))

    assignee: "User" = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    pass


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(sa_column=Column(String(length=32), index=True, unique=True))


class File(SQLModel, table=True):
    __tablename__ = "files"

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(sa_column=Column(String(length=255)))
    path: str = Field(sa_column=Column(String(length=255)))
    meeting_id: int = Field(foreign_key="meetings.id")

    meeting: "Meeting" = Relationship(back_populates="files")
