import asyncio

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.infrastructure.database import Base
from app.settings import Settings


@pytest.fixture
def settings():
    return Settings()


engine = create_async_engine(url='postgresql+asyncpg://postgres:1234@localhost:5433/pomodoro-test', future=True,
                             echo=True, pool_pre_ping=True)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_model(event_loop):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as cleanup_conn:
        await cleanup_conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def get_db_session() -> AsyncSession:
    return AsyncSessionFactory()
