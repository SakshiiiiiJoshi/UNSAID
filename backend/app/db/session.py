from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings

# asyncpg driver: postgresql+asyncpg://user:pass@host/db
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,   # Detect stale connections before use
    pool_size=10,
    max_overflow=20,
    echo=False,           # Set True temporarily for SQL debugging
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    """FastAPI dependency — yields an async DB session per request."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
