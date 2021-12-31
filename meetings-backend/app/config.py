from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    app_name: str
    database_url: str
    secret_key: str
    root_path: str = "/"
    allowed_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
