# TgBotTemplate

A minimal starting point for a Telegram bot: **aiogram 3**, **SQLAlchemy 2 (async)**, **Alembic**,
optional **Redis** FSM storage, Docker Compose.

One handler ships with it: `/start` greets the user and saves them to the `users` table.
Everything else is an empty module with a note about what belongs there.

## Quick start

```bash
cp .env.example .env          # then put your @BotFather token in BOT_TOKEN
make install
docker compose up -d postgres redis
make migrate
make run
```

`make help` lists every target.

## Layout

```
bot/
  main.py          entrypoint: builds Bot/Dispatcher, wires middlewares, starts polling
  config.py        pydantic-settings; validates the environment once at startup
  handlers/        start.py — the only handler; add a Router per feature
  middlewares/     db.py — one AsyncSession per update; add your own here
  keyboards/       empty
  filters/         empty
  states/          empty
  db/              declarative base, User model, engine/session factory
  utils/           logging setup, Telegram command menu
migrations/        Alembic (async env.py, DSN taken from bot.config)
```

## Adding a feature

1. Create `bot/handlers/<feature>.py` with `router = Router(name="<feature>")`.
2. Add it to `build_router()` in `bot/handlers/__init__.py` — aiogram stops at the first
   matching handler, so keep specific handlers above catch-alls.
3. New commands go in `bot/utils/commands.py` so they appear in the Telegram menu.

Handlers receive middleware values by parameter name — `session` comes from
`DbSessionMiddleware`:

```python
@router.message(Command("me"))
async def cmd_me(message: Message, session: AsyncSession) -> None:
    user = await session.get(User, message.from_user.id)
    await message.answer(f"You are {user.first_name}")
```

## Migrations

`migrations/env.py` reads the DSN from `bot.config`, so `alembic.ini` holds no URL and there is
nothing to keep in sync. Autogenerate only sees models imported by `bot/db/__init__.py`.

```bash
make migration m="add orders table"
make migrate
```

## Notes

- `REDIS_DSN` unset falls back to `MemoryStorage`, which loses FSM state on restart — fine for
  development, not for production.
- `DROP_PENDING_UPDATES=true` discards the backlog queued while the bot was down. Set it to
  `false` if missed updates matter.
- Long polling is the default. For webhooks, replace `dp.start_polling(...)` in `bot/main.py`
  with `aiogram.webhook.aiohttp_server`.
