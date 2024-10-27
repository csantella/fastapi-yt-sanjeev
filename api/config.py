from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_host: str
    database_port: str
    database_password: str = "load_later"
    database_name: str
    database_username: str
    secret_key: str
    token_algorithm: str
    access_token_expire_minutes: int


settings = Settings()