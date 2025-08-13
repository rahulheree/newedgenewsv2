from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    admin_username: str
    admin_password: str

    class Config:
        env_file = ".env"

settings = Settings()
