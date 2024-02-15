import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher, F, enums
from aiogram.fsm.storage.redis import RedisStorage
from config_data import Settings
from middlewares import DBMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


async def endpoint():
    """Endpoint for app"""

    ROOT_DIR = Path(__file__).absolute().parent.parent
    settings = Settings(_env_file=ROOT_DIR.joinpath(".env"))

    engine = create_async_engine(url=settings.pg_dsn, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

    bot = Bot(
        token=settings.bot_token.get_secret_value(),
        parse_mode=enums.ParseMode.HTML,
    )
    dp = Dispatcher(storage=RedisStorage.from_url(settings.redis_dsn))
    dp.update.middleware(DBMiddleware(session_pool=sessionmaker))
    dp.message.filter(F.chat.type == enums.ChatType.PRIVATE)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(endpoint())
