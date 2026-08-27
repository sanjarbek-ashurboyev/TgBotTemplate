"""Aggregates every feature router into one.

Add a router per feature module and include it below. aiogram stops at the first
matching handler, so keep specific handlers above catch-alls.
"""

from aiogram import Router

from bot.handlers import start


def build_router() -> Router:
    router = Router(name="root")
    router.include_routers(
        start.router,
    )
    return router


__all__ = ["build_router"]
