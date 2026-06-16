import logging
from contextlib import contextmanager
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from config import settings

logger = logging.getLogger("uvicorn.error")

# This variable will hold our connection pool instance globally
_pg_pool = None

def init_raw_db_pool():
    """Initializes the connection pool when the application starts."""
    global _pg_pool
    try:
        _pg_pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host=settings.DB_HOST,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            port=settings.DB_PORT
        )
        logger.info("Psycopg2 connection pool initialized successfully. 🔋")
    except Exception as e:
        logger.error(f"Failed to initialize Psycopg2 pool: {e}")
        raise e

def close_raw_db_pool():
    """Closes all connections in the pool when the application shuts down."""
    global _pg_pool
    if _pg_pool:
        _pg_pool.closeall()
        logger.info("Psycopg2 connection pool closed safely. 🔌")

@contextmanager
def get_raw_connection():
    """
    Context manager to safely lend out a connection from the pool.
    Automatically returns the connection to the pool when done, 
    even if an error occurs.
    """
    global _pg_pool
    if not _pg_pool:
        raise RuntimeError("Psycopg2 connection pool is not initialized.")
    
    connection = _pg_pool.getconn()
    try:
        yield connection
    finally:
        # Puts the connection back into the pool for another request to use
        _pg_pool.putconn(connection)