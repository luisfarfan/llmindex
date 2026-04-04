from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings and Environment Variables."""
    
    # Project Info
    PROJECT_NAME: str = "LLMIndex"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # API Keys
    OPENROUTER_API_KEY: str = "not-set"
    ARTIFICIAL_ANALYSIS_API_KEY: str = "not-set"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/llmindex.sqlite"

    # API Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

@lru_cache()
def get_settings() -> Settings:
    return Settings()
