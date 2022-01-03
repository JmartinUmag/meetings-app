from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from sqlmodel import Session

from app.database import get_db_session
from app.modules.auth.security import get_current_active_user
from app.modules.meetings.crud import (
    insert_file,
    insert_meeting,
    select_all_meetings,
    select_meeting_by_id,
)
from app.modules.meetings.models import File as FileModel
from app.modules.meetings.models import MeetingCreate, MeetingRead
from app.modules.meetings.utilities import generate_filename, save_file

router = APIRouter()


@router.get(
    "/meetings/",
    response_model=List[MeetingRead],
    dependencies=[Depends(get_current_active_user)],
)
async def get_meetings(session: Session = Depends(get_db_session)):
    return select_all_meetings(session)


@router.get(
    "/meetings/{meeting_id}",
    response_model=MeetingRead,
    dependencies=[Depends(get_current_active_user)],
)
async def get_meeting(meeting_id: int, session: Session = Depends(get_db_session)):
    return select_meeting_by_id(session, meeting_id)


@router.post(
    "/meetings/",
    response_model=MeetingRead,
    dependencies=[Depends(get_current_active_user)],
)
async def create_meeting(
    meeting: MeetingCreate, session: Session = Depends(get_db_session)
):
    return insert_meeting(session, meeting)


@router.post(
    "/meetings/{meeting_id}/add-file",
    response_model=FileModel,
    dependencies=[Depends(get_current_active_user)],
)
async def add_file(
    meeting_id: int,
    file: UploadFile = File(...),
    session: Session = Depends(get_db_session),
):
    filename = generate_filename(file.filename)

    # make the db record
    file_db = FileModel(name=file.filename, path=filename, meeting_id=meeting_id)
    file_db = insert_file(session, file_db)

    # save the file
    await save_file(file, filename)

    return file_db
