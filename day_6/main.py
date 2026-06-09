from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.connection_raw import init_raw_db_pool, close_raw_db_pool
from database.connection_orm import engine, Base
from routes import items_raw, items_orm

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Startup Logic: Initialize connection pools and build database tables
    init_raw_db_pool()
    Base.metadata.create_all(bind=engine)
    yield
    # 2. Shutdown Logic: Safely wipe and close out active database connection streams
    close_raw_db_pool()

app = FastAPI(
    title="FastAPI Database Integration Masterclass",
    version="1.0.0",
    lifespan=lifespan
)

# Connect our API routers to the main application app
app.include_router(items_raw.router)
app.include_router(items_orm.router)

@app.get("/")
def health_check():
    """Simple API status endpoint."""
    return {"status": "healthy", "database_integration": "active"}