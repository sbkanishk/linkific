import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="customer") # Options: 'admin' or 'customer'
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    # One-to-Many relationship with Products
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, index=True, nullable=False)
    stock = Column(Integer, nullable=False)
    image_url = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    category = relationship("Category", back_populates="products")

    # Safeguards and Constraints
    __table_args__ = (
        # Prevent a duplicate product name within the exact same category boundary
        UniqueConstraint('name', 'category_id', name='_name_category_uc'),
        # Ensure prices remain mathematically positive
        CheckConstraint('price > 0', name='_price_positive_cc'),
        # Enforce that stock reserves never slip below absolute zero
        CheckConstraint('stock >= 0', name='_stock_non_negative_cc'),
    )