from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_db_session
from app.modules.meetings.crud import (
    insert_meeting,
    select_all_meetings,
    select_meeting_by_id,
)
from app.modules.meetings.models import MeetingCreate, MeetingRead

router = APIRouter()


@router.get("/meetings/", response_model=List[MeetingRead])
async def get_meetings(session: Session = Depends(get_db_session)):
    return select_all_meetings(session)


@router.get("/meetings/{meeting_id}", response_model=MeetingRead)
async def get_meeting(meeting_id: int, session: Session = Depends(get_db_session)):
    return select_meeting_by_id(session, meeting_id)


@router.post("/meetings/", response_model=MeetingRead)
async def create_meeting(
    meeting: MeetingCreate, session: Session = Depends(get_db_session)
):
    return insert_meeting(session, meeting)
