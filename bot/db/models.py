"""ORM models. Add your own tables here."""

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """A Telegram user, saved on /start."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    username: Mapped[str | None] = mapped_column(String(32), index=True)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str | None] = mapped_column(String(64))
    language_code: Mapped[str | None] = mapped_column(String(8))

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"
