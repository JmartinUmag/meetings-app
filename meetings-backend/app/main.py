import uvicorn
from fastapi import FastAPI

from app.modules.auth.api import router as auth_router
from app.modules.meetings.api import router as meetings_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(meetings_router, prefix="/meetings", tags=["meetings"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
