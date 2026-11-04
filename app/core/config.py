from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Proveedor
    LLM_PROVIDER: str = "OPENROUTER"

    # OpenRouter
    OPENROUTER_API_KEY: str
    OPENROUTER_MODEL: str = "openai/gpt-4o"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    # Otros proveedores (opcionales)
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4o"

    GOOGLE_API_KEY: str | None = None
    GOOGLE_MODEL: str = "gemini-1.5-pro"

    GROQ_API_KEY: str | None = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
