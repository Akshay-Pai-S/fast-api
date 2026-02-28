from datetime import datetime
from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Integer, String, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Post(Base):
    __tablename__ = 'posts'

    id : Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    published: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text('false')
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    owner_id : Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    owner = relationship ("User")

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )

    password: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )