from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):

	model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

	APP_NAME: str
	APP_VERSION: str
	APP_ENV: str
	FILE_ALLOWED_TYPES: list[str]
	FILE_MAX_SIZE: int

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
# You can access settings like this:
# settings.APP_NAME
