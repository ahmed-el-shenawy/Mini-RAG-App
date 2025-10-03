from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str
    APP_VERSION: str
    APP_ENV: str
    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    MONGODB_URL: str
    MONGODB_DATABASE: str

    GENERATION_BACKEND:str
    EMBEDDING_BACKEND:str

    OPENAI_API_KEY:str
    OPENAI_API_BASE_URL:str
    COHERE_API_KEY:str

    COHERE_EMBEDDING_MODEL:str
    EMBEDDING_MODEL_SIZE:int
    OPENAI_GENERATION_MODEL:str

    DEFAULT_INPUT_MAX_TOKENS:int
    DEFAULT_OUTPUT_MAX_TOKENS:int
    OPENAI_TEMPERATURE:float

    VECTOR_DB_BACKEND:str
    VECTOR_DB_METRIC:str
    QDRANT_DB_PATH:str

@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore


settings = get_settings()
# You can access settings like this:
# settings.APP_NAME
