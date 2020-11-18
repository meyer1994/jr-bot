from pydantic import BaseSettings


class Telegram(BaseSettings):
    token: str = 'token'

    class Config:
        env_prefix = 'telegram_'
        env_file = '.env'


class Google(BaseSettings):
    bucket: str = 'bucket'

    class Config:
        env_prefix = 'google_'
        env_file = '.env'


class Algolia(BaseSettings):
    user: str = 'user'
    token: str = 'token'
    index: str = 'index'

    class Config:
        env_prefix = 'algolia_'
        env_file = '.env'
