from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from database import db_manager, MONGO_URL
from routes import router as student_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles the startup and shutdown lifecycle events.
    Ensures we maintain a single connection pool across requests.
    """
    # 1. Action on Startup: Initialize the global Motor Client
    db_manager.client = AsyncIOMotorClient(MONGO_URL)
    print("========================================")
    print("🚀 Connected to MongoDB inside Docker successfully!")
    print("========================================")

    # Creating a background database index using pymongo style syntax through motor
    # This optimizes performance for searches checking emails
    await db_manager.client.student_db["students"].create_index("email", unique=True)

    yield # The app stays open and runs requests here

    # 2. Action on Shutdown: Close the database connection safely
    db_manager.client.close()
    print("========================================")
    print("🔌 MongoDB connection closed safely.")
    print("========================================")

# Create our FastAPI application instance and hook up our lifecycle manager
app = FastAPI(
    title="FastAPI MongoDB Student Management System",
    description="Day 9 Assignment: Async CRUD operations, Embedding, Referencing, and Indexing.",
    version="1.0.0",
    lifespan=lifespan
)

# Include our student router operations layer
app.include_router(student_router)

# Base test route to verify the web server is responsive
@app.get("/")
def read_root():
    return {"status": "online", "message": "Welcome to the FastAPI MongoDB Server"}