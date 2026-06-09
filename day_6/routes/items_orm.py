from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import exc
from typing import Optional
from database.connection_orm import get_db
from database import models

router = APIRouter(prefix="/orm/items", tags=["SQLAlchemy ORM Operations"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_item_orm(title: str, description: str, price: int, owner_id: int, db: Session = Depends(get_db)):
    """Creates a new record inside the items table using the ORM."""
    try:
        db_item = models.Item(title=title, description=description, price=price, owner_id=owner_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Integrity constraint violation. Check if the owner_id exists!"
        )

@router.get("/")
def read_items_orm(
    search: Optional[str] = None,
    sort_by: str = Query("id", enum=["id", "title", "price", "created_at"]),
    sort_order: str = Query("asc", enum=["asc", "desc"]),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Fetches list with integrated search filtering, sorting, and pagination."""
    # Only pull items that have NOT been soft-deleted
    query = db.query(models.Item).filter(models.Item.is_deleted == False)
    
    # Text Search Filter
    if search:
        query = query.filter(models.Item.title.ilike(f"%{search}%"))
    
    # Sorting Strategy
    order_column = getattr(models.Item, sort_by)
    if sort_order == "desc":
        order_column = order_column.desc()
    query = query.order_by(order_column)
    
    # Pagination Window
    return query.offset(offset).limit(limit).all()

@router.get("/{item_id}")
def read_single_item(item_id: int, db: Session = Depends(get_db)):
    """Queries a single record by its specific ID."""
    item = db.query(models.Item).filter(models.Item.id == item_id, models.Item.is_deleted == False).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found or soft-deleted.")
    return item

@router.put("/{item_id}")
def update_item_orm(item_id: int, title: str, description: str, price: int, db: Session = Depends(get_db)):
    """Updates an existing item's records."""
    item = db.query(models.Item).filter(models.Item.id == item_id, models.Item.is_deleted == False).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")
    
    item.title = title
    item.description = description
    item.price = price
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def soft_delete_item_orm(item_id: int, db: Session = Depends(get_db)):
    """Performs a safe soft-delete operation by flipping the boolean flag."""
    item = db.query(models.Item).filter(models.Item.id == item_id, models.Item.is_deleted == False).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")
    
    item.is_deleted = True
    db.commit()
    return None