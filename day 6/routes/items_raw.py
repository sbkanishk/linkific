from fastapi import APIRouter, HTTPException, status
from psycopg2.extras import RealDictCursor
import psycopg2
from database.connection_raw import get_raw_connection

router = APIRouter(prefix="/raw/items", tags=["Raw SQL Operations"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_item_raw(title: str, description: str, price: int, owner_id: int):
    """Creates a new item using raw parameterized SQL queries."""
    with get_raw_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            try:
                # Use %s placeholders to prevent SQL Injection
                query = """
                    INSERT INTO items (title, description, price, owner_id, is_deleted)
                    VALUES (%s, %s, %s, %s, False)
                    RETURNING id, title, description, price, owner_id, is_deleted;
                """
                cur.execute(query, (title, description, price, owner_id))
                new_item = cur.fetchone()
                
                # Commit the transaction explicitly
                conn.commit()  
                return new_item
                
            except psycopg2.errors.UniqueViolation:
                conn.rollback()
                raise HTTPException(status_code=400, detail="Unique constraint violated.")
            except Exception as e:
                # Rollback changes if anything goes wrong
                conn.rollback()  
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/")
def read_items_raw(limit: int = 10, offset: int = 0):
    """Fetches a paginated list of non-deleted items using raw SQL."""
    with get_raw_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = """
                SELECT id, title, description, price, owner_id 
                FROM items 
                WHERE is_deleted = False 
                LIMIT %s OFFSET %s;
            """
            cur.execute(query, (limit, offset))
            return cur.fetchall()