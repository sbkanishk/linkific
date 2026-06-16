import os
from motor.motor_asyncio import AsyncIOMotorClient

# This points directly to the MongoDB instance running inside your Docker container
MONGO_URL = "mongodb://localhost:27017"

class DatabaseManager:
    client: AsyncIOMotorClient = None

db_manager = DatabaseManager()

def get_database():
    """
    Dependency function that returns our database instance.
    FastAPI will inject this into our API endpoints.
    """
    return db_manager.client.student_db
