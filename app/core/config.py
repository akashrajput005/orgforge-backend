from pydantic import BaseSettings


class Settings(BaseSettings):
    mongodb_uri: str
    master_db: str = "org_master"

    jwt_secret: str
    jwt_algo: str = "HS256"
    jwt_exp_seconds: int = 3600

    app_host: str = "0.0.0.0"
    app_port: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()
