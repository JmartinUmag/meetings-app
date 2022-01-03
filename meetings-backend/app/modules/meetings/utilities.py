import re
import uuid
from os import makedirs, path
from tempfile import TemporaryFile

from aiofiles import open as aio_open

from app.config import settings


def generate_filename(filename) -> str:
    extension = re.sub(r"^[^.]+\.", "", filename)
    file_path = f"{uuid.uuid4().hex}.{extension}"

    return file_path


async def save_file(file: TemporaryFile, filename: str):
    makedirs(settings.uploads_directory, exist_ok=True)

    async with aio_open(path.join(settings.uploads_directory, filename), "wb") as f:
        content = await file.read()
        await f.write(content)
