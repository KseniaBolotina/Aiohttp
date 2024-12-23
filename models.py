import datetime
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, func

POSTGRES_USER = os.getenv('POSTGRES_USER', 'user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '1234')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'aiohttp')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')

POSTGRES_DSN = (f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')
engine = create_async_engine(POSTGRES_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    @property
    def id_dict(self):
        return {'id':self.id }
    #pass

class Ad(Base):
    __tablename__ = 'app_ad'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    header: Mapped[str] = mapped_column(String, index=True, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner: Mapped[str] = mapped_column(String, nullable=False)

    @property
    def dict(self):
        return {
            'id': self.id,
            'header': self.header,
            'description': self.description,
            'created_date': self.created_date.isoformat(),
            'owner': self.owner
        }

async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()