import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.config import settings
from app.modules.auth.api import router as auth_router
from app.modules.meetings.api import router as meetings_router

if not settings.debug:
    docs_opts = {"docs_url": None, "redoc_url": None}
else:
    docs_opts = {}

app = FastAPI(title=settings.app_name, root_path=settings.root_path, **docs_opts)

app.mount(
    settings.uploads_baseurl,
    StaticFiles(directory=settings.uploads_directory),
    name="uploads",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(meetings_router, prefix="/meetings", tags=["meetings"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
