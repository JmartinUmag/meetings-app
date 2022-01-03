from typing import List

from sqlalchemy import select
from sqlmodel import Session

from app.modules.auth.crud import select_user_by_id
from app.modules.meetings.models import File, Meeting, MeetingCreate


def select_all_meetings(session: Session) -> List[Meeting]:
    return session.execute(select(Meeting)).scalars().all()


def select_meeting_by_id(session: Session, meeting_id: int) -> Meeting:
    return session.get(Meeting, meeting_id)


def insert_meeting(session: Session, meeting: MeetingCreate) -> Meeting:
    meeting_db = Meeting(**meeting.dict(exclude={"assistants_ids": True}))
    for user_id in meeting.assistants_ids:
        user = select_user_by_id(session, user_id)
        # if user does not exist, skip it
        if user is not None:
            meeting_db.assistants.append(user)

    session.add(meeting_db)
    session.commit()

    return meeting_db


def select_file_by_id(session: Session, file_id: int) -> File:
    return session.get(File, file_id)


def insert_file(session: Session, file: File) -> File:
    session.add(file)
    session.commit()

    return file
