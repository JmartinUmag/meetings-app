from typing import List, Optional

from sqlmodel import Column, Field, Relationship, SQLModel, String

from app.modules.meetings.models import Meeting, MeetingUserLink


class UserBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column(String(32)))
    fullname: str = Field(sa_column=Column(String(64)))
    enabled: bool = Field(default=True)


class User(UserBase, table=True):
    __tablename__ = "users"

    password: str = Field(sa_column=Column(String(128)))

    meetings: List["Meeting"] = Relationship(
        back_populates="assistants", link_model=MeetingUserLink
    )


class UserRead(UserBase):
    pass


class APIToken(SQLModel):
    access_token: str
    token_type: str
