from typing import Annotated

from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import config

engine = create_async_engine(url=config.database.sqlalchemy_url(),
                             echo=True)

async_session = async_sessionmaker(engine)

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[str]
    date: Mapped[str]


class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)


class Tariff(Base):
    __tablename__ = 'tariffs'

    id: Mapped[intpk]
    title: Mapped[str]
    price: Mapped[int]
    month_count: Mapped[int]


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)
    start_date: Mapped[str]
    end_date: Mapped[str]
    client_id: Mapped[str]


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
