"""The command list Telegram shows in the client's menu button.

Add a BotCommand here for every command you register a handler for.
"""

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

COMMANDS = [
    BotCommand(command="start", description="Start the bot"),
]


async def set_bot_commands(bot: Bot) -> None:
    """Called once on startup; Telegram persists this server-side."""
    await bot.set_my_commands(COMMANDS, scope=BotCommandScopeAllPrivateChats())
