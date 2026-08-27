"""Entrypoint: builds the bot, wires middlewares and routers, starts polling."""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from bot.config import Settings, get_settings
from bot.db import create_engine, create_session_factory
from bot.handlers import build_router
from bot.middlewares import DbSessionMiddleware
from bot.utils import set_bot_commands, setup_logging

logger = logging.getLogger(__name__)


def build_storage(settings: Settings) -> BaseStorage:
    if settings.redis_dsn:
        return RedisStorage.from_url(settings.redis_dsn)
    logger.warning("REDIS_DSN is unset: FSM state is in memory and is lost on restart")
    return MemoryStorage()


async def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)

    engine = create_engine(settings.db_dsn, echo=settings.db_echo)
    session_factory = create_session_factory(engine)
    storage = build_storage(settings)

    bot = Bot(
        token=settings.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    # Extra kwargs are injected into every handler's arguments by name.
    dp = Dispatcher(storage=storage, settings=settings)

    # Outer middlewares run before filters. Register your own here.
    dp.update.outer_middleware(DbSessionMiddleware(session_factory))

    dp.include_router(build_router())

    await set_bot_commands(bot)
    logger.info("starting polling")
    try:
        await dp.start_polling(
            bot,
            # Ask Telegram only for update types some handler actually subscribes to.
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=settings.drop_pending_updates,
        )
    finally:
        await storage.close()
        await bot.session.close()
        await engine.dispose()
        logger.info("shutdown complete")


def run() -> None:
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("stopped by user")


if __name__ == "__main__":
    run()
