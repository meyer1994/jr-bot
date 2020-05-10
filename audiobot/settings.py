from pydantic import BaseSettings


class AlgoliaSettings(BaseSettings):
    algolia_user: str = 'user'
    algolia_token: str = 'token'
    algolia_index: str = 'index'

    class Config:
        env_file = '.env'
        env_prefix = 'algolia_'


class GoogleSettings(BaseSettings):
    storage_bucket: str = 'bucket'

    class Config:
        env_prefix = 'google_'
        env_file = '.env'


class TelegramSettings(BaseSettings):
    token: str = 'token'

    class Config:
        env_prefix = 'telegram_'
        env_file = '.env'
