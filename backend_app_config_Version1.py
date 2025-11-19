from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    REDIS_URL: str = Field(..., env="REDIS_URL")
    RABBITMQ_URL: str = Field(..., env="RABBITMQ_URL")
    JWT_SECRET: str = Field("changeme", env="JWT_SECRET")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    MODEL_DIR: str = Field("/app/models", env="MODEL_DIR")
    MEDIA_DIR: str = Field("/app/storage", env="MEDIA_DIR")
    APP_HOST: str = Field("0.0.0.0", env="APP_HOST")
    APP_PORT: int = Field(8000, env="APP_PORT")
    ADMIN_USERNAME: str = Field("admin", env="ADMIN_USERNAME")
    ADMIN_PASSWORD: str = Field("admin", env="ADMIN_PASSWORD")

    class Config:
        env_file = ".env"


settings = Settings()