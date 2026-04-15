from fastapi import FastAPI
from app.api.routes import auth, services, customers, bookings, dashboard
from app.db.session import engine
from app.db.base import Base
from app.core.logger import setup_logger
from app.middleware.error_handler import ErrorHandlerMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.core.limiter import limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI()




setup_logger()


app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # "http://localhost:3000",
        # "http://127.0.0.1:3000",
        # "http://localhost:5173",  
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(services.router)
app.include_router(customers.router)
app.include_router(bookings.router)
app.include_router(dashboard.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)