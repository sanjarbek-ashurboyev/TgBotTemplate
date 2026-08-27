# Add your own middlewares here (throttling, logging, i18n) and register them
# in bot/main.py.

from bot.middlewares.db import DbSessionMiddleware

__all__ = ["DbSessionMiddleware"]
