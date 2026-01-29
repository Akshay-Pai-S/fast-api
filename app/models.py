from datetime import datetime
from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

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