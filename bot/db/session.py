"""Engine and session factory construction."""

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def create_engine(dsn: str, *, echo: bool = False) -> AsyncEngine:
    return create_async_engine(
        dsn,
        echo=echo,
        pool_pre_ping=True,  # survives connections dropped by the DB or a proxy
    )


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,  # attributes stay usable after commit inside handlers
        autoflush=False,
    )
