from dataclasses import dataclass
from environs import Env


# Конфиг бота
@dataclass
class TgBot:
    token: str


# Конфиг для pyrogram
@dataclass
class TgAPI:
    username: str
    api_id: str
    api_hash: str


# Конфиг для базы данных
@dataclass
class Database:
    name: str
    echo: bool


# Глобальный конфиг
@dataclass
class Config:
    tg_bot: TgBot
    tg_api: TgAPI
    db: Database


# Получение конфига
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
            echo=env.bool('BD_ECHO', False)
        )
    )
