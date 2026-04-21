from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    APP_NAME: str = Field(default="RS Education Solution - Resume Builder")
    APP_VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=False)
    GROQ_API_KEY: str = Field(..., env="GROQ_API_KEY")
    # After (current production model)
    # Using 8B as primary for speed and higher rate limits
    GROQ_MODEL: str = Field(default="llama-3.1-8b-instant")
    GROQ_FALLBACK_MODEL: str = Field(default="llama-3.3-70b-versatile")
    GROQ_TEMPERATURE: float = Field(default=0.3)
    GROQ_MAX_TOKENS: int = Field(default=4096)
    
    # Retry and Throttling Settings
    MAX_RETRIES: int = Field(default=3)
    RETRY_DELAY_MIN: int = Field(default=4)
    RETRY_DELAY_MAX: int = Field(default=10)
    RATE_LIMIT_GENERATION: str = Field(default="2/minute")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
