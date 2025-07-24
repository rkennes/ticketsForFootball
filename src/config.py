from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str
    database_url: str
    sync_database_url: str  

    class Config:
        env_file = ".env"

settings = Settings()
