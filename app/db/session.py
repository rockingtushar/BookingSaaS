from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

engine = create_async_engine(settings.DATABASE_URL, echo=True, pool_pre_ping=True, pool_size=5, max_overflow=10, connect_args={"ssl": ssl_context})

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()  
            raise