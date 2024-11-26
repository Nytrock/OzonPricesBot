from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class TgAPI:
    username: str
    api_id: str
    api_hash: str


@dataclass
class Database:
    name: str
    echo: bool


@dataclass
class Config:
    tg_bot: TgBot
    tg_api: TgAPI
    db: Database


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        ),
        tg_api=TgAPI(
            username=env('TELEGRAM_API_USERNAME'),
            api_id=env('TELEGRAM_API_ID'),
            api_hash=env('TELEGRAM_API_HASH')
        ),
        db=Database(
            name=env('BD_NAME'),
            echo=bool(env('BD_ECHO'))
        )
    )
