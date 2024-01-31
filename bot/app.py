import asyncio

from aiogram import Bot, Dispatcher, enums
from config import app_config


async def endpoint():
    """Endpoint for app"""

    bot = Bot(
        token=app_config.bot_token.get_secret_value(),
        parse_mode=enums.ParseMode.HTML,
    )
    dp = Dispatcher()

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(endpoint())
