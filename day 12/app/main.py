from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, exc
from typing import List, Optional

from .database import engine, Base, get_db
from .models import User, Category, Product
from .schemas import (
    UserCreate, UserResponse, Token, CategoryCreate, CategoryResponse, 
    ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
)
from .auth import hash_password, verify_password, create_access_token, require_admin, get_current_user

# Initialize database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Day 12 E-Commerce Ecosystem API")

# ==========================================
# AUTHENTICATION ENDPOINTS
# ==========================================
@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check for existing credentials
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role=user_in.role if user_in.role in ["admin", "customer"] else "customer"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=Token)
def login(form_data: UserCreate, db: Session = Depends(get_db)):  # Custom body object match for ease
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}


# ==========================================
# CATEGORIES API
# ==========================================
@app.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    if db.query(Category).filter(Category.name == category.name).first():
        raise HTTPException(status_code=400, detail="Category name already exists")
    
    new_cat = Category(**category.model_dump())
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat

@app.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@app.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, update_data: CategoryCreate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category location not found")
    
    # Verify name updates do not clash with independent existing categories
    existing = db.query(Category).filter(Category.name == update_data.name, Category.id != category_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Another category already uses this name")
        
    cat.name = update_data.name
    cat.description = update_data.description
    db.commit()
    db.refresh(cat)
    return cat

@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category location not found")
    db.delete(cat)
    db.commit()


# ==========================================
# PRODUCTS API (WITH SEARCH & FILTER)
# ==========================================
@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    # Verify target category exists
    if not db.query(Category).filter(Category.id == product.category_id).first():
        raise HTTPException(status_code=404, detail="Target category does not exist")
    
    try:
        new_prod = Product(**product.model_dump())
        db.add(new_prod)
        db.commit()
        db.refresh(new_prod)
        return new_prod
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Product name already exists within this category boundary.")

@app.get("/products", response_model=List[ProductListResponse])
def get_products(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = Query("date", enum=["price_asc", "price_desc", "name", "date"])
):
    query = db.query(Product)
    
    # 🔍 Dynamic Search Rule
    if search:
        query = query.filter(or_(Product.name.ilike(f"%{search}%"), Product.description.ilike(f"%{search}%")))
    
    # 🗂️ Category and Pricing Filters
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
        
    # 📊 Sort Parameters
    if sort_by == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort_by == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort_by == "name":
        query = query.order_by(Product.name.asc())
    else:
        query = query.order_by(Product.created_at.desc())
        
    # 📜 Pagination Mechanics
    offset = (page - 1) * limit
    return query.offset(offset).limit(limit).all()

@app.get("/products/{product_id}", response_model=ProductListResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product entity not found")
    return prod

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, update_data: ProductUpdate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product entity not found")
        
    for key, val in update_data.model_dump(exclude_unset=True).items():
        setattr(prod, key, val)
        
    try:
        db.commit()
        db.refresh(prod)
        return prod
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Update causes a database conflict (e.g. naming constraint violation).")

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product entity not found")
    db.delete(prod)
    db.commit()


@app.get("/categories/{category_id}/products", response_model=List[ProductResponse])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    if not db.query(Category).filter(Category.id == category_id).first():
        raise HTTPException(status_code=404, detail="Category location not found")
    return db.query(Product).filter(Product.category_id == category_id).all()