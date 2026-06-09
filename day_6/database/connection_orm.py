from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

# 1. Create the SQLAlchemy engine 
# pool_size controls how many stable connections are kept open
engine = create_engine(
    settings.DATABASE_URL_SQLALCHEMY(),
    pool_size=5,
    max_overflow=10,
    echo=False  # Set to True if you want to see all auto-generated SQL in your terminal
)

# 2. Create a session factory
# This will be used to spin up discrete database sessions per API request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Create the Declarative Base class
# All our database model classes will inherit from this class to map to tables
Base = declarative_base()

def get_db():
    """
    Dependency injection generator function.
    Creates a new database session for a single API request, 
    and automatically closes it after the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()