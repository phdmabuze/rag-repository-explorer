from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    chunk_size: int = 1000
    chunk_overlap: int = 200

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
