from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    app_name: str
    database_url: str
    secret_key: str
    root_path: str = "/"
    allowed_origins: List[str] = ["*"]
    uploads_directory: str = "./storage"
    uploads_baseurl: str = "/storage"

    class Config:
        env_file = ".env"


settings = Settings()
