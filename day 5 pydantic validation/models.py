from pydantic import BaseModel, Field, EmailStr, HttpUrl, field_validator, model_validator
from typing import List, Optional, Annotated
from datetime import datetime
from enum import Enum
import re

# ==================================================
# ENUMS
# ==================================================

class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"

class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class ProductCategory(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    food = "food"
    books = "books"
    other = "other"

# ==================================================
# 1. NESTED CONFIGURATION: ADDRESS & USER SCHEMAS
# ==================================================

class Address(BaseModel):
    street: str = Field(..., examples=["123 Main St"])
    city: str = Field(..., min_length=2)
    zip_code: str = Field(..., pattern=r"^\d{5}(-\d{4})?$")
    country: str = Field(default="India", min_length=2)

# ---------- User: Create ----------
class UserCreate(BaseModel):
    """Model used for incoming registration (POST requests)."""
    username: str = Field(..., min_length=4, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(..., min_length=8)
    age: int = Field(..., ge=18, le=120)  # ge/le instead of gte/lte (Pydantic V2)
    address: Address  # Nested model

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*]", v):
            raise ValueError("Password must contain at least one special character (!@#$%^&*)")
        return v

    @field_validator("username")
    @classmethod
    def username_not_reserved(cls, v: str) -> str:
        reserved = {"admin", "root", "system", "superuser"}
        if v.lower() in reserved:
            raise ValueError(f"Username '{v}' is reserved")
        return v

# ---------- User: Update ----------
class UserUpdate(BaseModel):
    """Model for PATCH requests — all fields optional."""
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(default=None, ge=18, le=120)
    address: Optional[Address] = None

# ---------- User: Response ----------
class UserResponse(BaseModel):
    """Safe model returned in API responses — no password."""
    id: int
    username: str
    email: EmailStr
    age: int
    role: UserRole = UserRole.user
    address: Address
    created_at: datetime

# ==================================================
# 2. PRODUCT MODELS
# ==================================================

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    price: float = Field(..., gt=0, le=1_000_000)
    stock: int = Field(..., ge=0)
    category: ProductCategory
    image_url: Optional[HttpUrl] = None

    @field_validator("price")
    @classmethod
    def round_price(cls, v: float) -> float:
        return round(v, 2)

    @field_validator("name")
    @classmethod
    def name_no_special_chars(cls, v: str) -> str:
        if re.search(r"[<>\"'&]", v):
            raise ValueError("Product name contains invalid characters")
        return v.strip()

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    price: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    category: Optional[ProductCategory] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category: ProductCategory
    in_stock: bool = False  # Derived field — set by model_validator

    @model_validator(mode="after")
    def set_in_stock(self) -> "ProductResponse":
        self.in_stock = self.stock > 0
        return self

# ==================================================
# 3. ORDER MODELS (nested list of items)
# ==================================================

class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1)
    unit_price: float = Field(..., gt=0)

    @property
    def subtotal(self) -> float:
        return round(self.unit_price * self.quantity, 2)

class OrderCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    items: List[OrderItem] = Field(..., min_length=1)
    discount_percent: float = Field(default=0.0, ge=0, le=100)
    notes: Optional[str] = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def validate_totals_and_products(self) -> "OrderCreate":
        # Ensure no duplicate product IDs
        product_ids = [item.product_id for item in self.items]
        if len(product_ids) != len(set(product_ids)):
            raise ValueError("Duplicate product IDs in order items")
        return self

    @property
    def total_before_discount(self) -> float:
        return round(sum(item.subtotal for item in self.items), 2)

    @property
    def total_after_discount(self) -> float:
        discount = self.total_before_discount * (self.discount_percent / 100)
        return round(self.total_before_discount - discount, 2)

class OrderResponse(BaseModel):
    id: int
    user_id: int
    items: List[OrderItem]
    status: OrderStatus = OrderStatus.pending
    total: float
    created_at: datetime

# ==================================================
# 4. BLOG POST MODELS (with comments)
# ==================================================

class Comment(BaseModel):
    author_id: int
    content: str = Field(..., min_length=1, max_length=2000)
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator("content")
    @classmethod
    def no_empty_content(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Comment content cannot be blank")
        return v.strip()

class BlogPostCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=50)
    author_id: int = Field(..., gt=0)
    tags: List[str] = Field(default=[], max_length=10)
    publication_date: Optional[datetime] = None
    is_published: bool = False

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: List[str]) -> List[str]:
        cleaned = [tag.strip().lower() for tag in v]
        if any(len(tag) < 2 for tag in cleaned):
            raise ValueError("Each tag must be at least 2 characters")
        return list(set(cleaned))  # deduplicate

    @field_validator("title")
    @classmethod
    def title_not_clickbait(cls, v: str) -> str:
        clickbait = ["you won't believe", "shocking", "this will blow your mind"]
        if any(phrase in v.lower() for phrase in clickbait):
            raise ValueError("Title appears to be clickbait")
        return v.strip()

class BlogPostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    tags: List[str]
    comments: List[Comment] = []
    comment_count: int = 0
    publication_date: Optional[datetime]
    is_published: bool

    @model_validator(mode="after")
    def sync_comment_count(self) -> "BlogPostResponse":
        self.comment_count = len(self.comments)
        return self

# ==================================================
# 5. PAYMENT MODEL (cross-field validation)
# ==================================================

class PaymentCreate(BaseModel):
    card_number: str = Field(..., pattern=r"^\d{16}$")
    expiry_month: int = Field(..., ge=1, le=12)
    expiry_year: int = Field(..., ge=2024, le=2040)
    cvv: str = Field(..., pattern=r"^\d{3,4}$")
    amount: float = Field(..., gt=0)
    currency: str = Field(default="INR", pattern=r"^[A-Z]{3}$")

    @model_validator(mode="after")
    def validate_card_not_expired(self) -> "PaymentCreate":
        now = datetime.now()
        if self.expiry_year < now.year or (
            self.expiry_year == now.year and self.expiry_month < now.month
        ):
            raise ValueError("Card is expired")
        return self

    @field_validator("card_number")
    @classmethod
    def luhn_check(cls, v: str) -> str:
        """Basic Luhn algorithm check."""
        digits = [int(d) for d in v]
        digits.reverse()
        total = sum(
            d if i % 2 == 0 else (d * 2 - 9 if d * 2 > 9 else d * 2)
            for i, d in enumerate(digits)
        )
        if total % 10 != 0:
            raise ValueError("Invalid card number (failed Luhn check)")
        return v