from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# We use a local SQLite database file named 'ecommerce.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///./ecommerce.db"

# Create the database engine
engine = create_engine(
    # connect_args={"check_same_thread": False} is required only for SQLite
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for our database models to inherit from
Base = declarative_base()

# Dependency utility to get a DB session context per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()