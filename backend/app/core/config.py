from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"

    llm_provider: str = "ollama"

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma-4b"

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"

    github_token: str | None = None
    github_owner: str | None = None
    github_repo: str | None = None

    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()