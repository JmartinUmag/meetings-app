from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    database_url: str
    secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()
