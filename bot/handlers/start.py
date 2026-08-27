"""/start — greets the user and saves their info."""

from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession) -> None:
    # `session` is injected by DbSessionMiddleware, registered in bot/main.py.
    tg_user = message.from_user
    if tg_user is None:
        return

    values = {
        "id": tg_user.id,
        "username": tg_user.username,
        "first_name": tg_user.first_name,
        "last_name": tg_user.last_name,
        "language_code": tg_user.language_code,
    }
    # Upsert: one round trip, and safe if the user presses /start twice.
    await session.execute(
        insert(User)
        .values(**values)
        .on_conflict_do_update(
            index_elements=[User.id],
            set_={k: v for k, v in values.items() if k != "id"},
        )
    )
    await session.commit()

    await message.answer(f"Hello, {html.bold(tg_user.full_name)}!")
