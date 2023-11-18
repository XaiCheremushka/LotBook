from pydantic_settings import BaseSettings
from pydantic import SecretStr
import os


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    OPENAI_API_KEY: SecretStr

    WEBHOOK_HOST: str = 'host'
    WEBHOOK_PATH: str = f'/webhook/'

    WEBAPP_HOST: str
    WEBAPP_PORT: int = 80

    PATH_FIREBASE_KEY: str

    class Config:
        env_file = os.getcwd() + r'\tgbot\utiles\secretData\.env'
        env_file_encoding = 'utf-8'


config = Settings()