from pydantic import ValidationError
from datetime import datetime
from models import (
    Address, UserCreate, UserUpdate, UserResponse,
    ProductCreate, ProductUpdate, ProductResponse,
    OrderCreate, OrderItem, OrderResponse,
    BlogPostCreate, BlogPostResponse, Comment,
    PaymentCreate,
    UserRole, OrderStatus, ProductCategory
)

def separator(title: str):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print('='*55)

# ==================================================
# 1. VALID USER CREATION
# ==================================================
separator("1. UserCreate — Valid")
user = UserCreate(
    username="kanishk_sb",
    email="kanishk@example.com",
    password="SecurePass1!",
    age=20,
    address=Address(street="12 NIT Campus", city="Surat", zip_code="39500")
)
print(user.model_dump())

# ==================================================
# 2. USER VALIDATION ERRORS
# ==================================================
separator("2. UserCreate — Validation Errors")

test_cases = [
    # (description, kwargs)
    ("Weak password (no uppercase)", dict(
        username="testuser", email="t@t.com",
        password="weakpass1!", age=20,
        address=Address(street="x", city="Surat", zip_code="39500")
    )),
    ("Underage user (age=16)", dict(
        username="younguser", email="y@y.com",
        password="Strong1!@", age=16,
        address=Address(street="x", city="Surat", zip_code="39500")
    )),
    ("Reserved username", dict(
        username="admin", email="a@a.com",
        password="Strong1!@", age=22,
        address=Address(street="x", city="Surat", zip_code="39500")
    )),
]

for desc, kwargs in test_cases:
    try:
        UserCreate(**kwargs)
    except ValidationError as e:
        print(f"\n[{desc}]")
        for err in e.errors():
            print(f"  Field: {err['loc']} → {err['msg']}")

# ==================================================
# 3. PRODUCT MODELS
# ==================================================
separator("3. ProductCreate + ProductResponse")
product = ProductCreate(
    name="Wireless Mouse",
    price=599.99,
    stock=50,
    category=ProductCategory.electronics,
)
print("Created:", product.model_dump())

# ProductResponse with derived in_stock field
response = ProductResponse(id=1, name="Wireless Mouse", price=599.99, stock=0, category=ProductCategory.electronics)
print("In stock:", response.in_stock)  # False — derived from stock=0

# ==================================================
# 4. ORDER WITH NESTED ITEMS
# ==================================================
separator("4. OrderCreate — Nested items + cross-field validation")
order = OrderCreate(
    user_id=1,
    items=[
        OrderItem(product_id=1, quantity=2, unit_price=599.99),
        OrderItem(product_id=2, quantity=1, unit_price=199.00),
    ],
    discount_percent=10
)
print(f"Items: {len(order.items)}")
print(f"Total before discount: ₹{order.total_before_discount}")
print(f"Total after 10% discount: ₹{order.total_after_discount}")

# Duplicate product IDs — should fail
separator("4b. OrderCreate — Duplicate product IDs (should fail)")
try:
    bad_order = OrderCreate(
        user_id=1,
        items=[
            OrderItem(product_id=5, quantity=1, unit_price=100),
            OrderItem(product_id=5, quantity=2, unit_price=100),
        ]
    )
except ValidationError as e:
    for err in e.errors():
        print(f"  Error: {err['msg']}")

# ==================================================
# 5. BLOG POST WITH TAGS + COMMENTS
# ==================================================
separator("5. BlogPostCreate — Tags deduplication & validation")
post = BlogPostCreate(
    title="Understanding Power Laws in Football",
    content="Power laws appear in football scoring distributions when we analyze " +
            "elite players like Messi and Ronaldo versus the rest. " * 3,
    author_id=1,
    tags=["football", "data", "football", "analytics"],  # duplicate tag
    is_published=True
)
print("Tags (deduped):", post.tags)

# ==================================================
# 6. USER UPDATE (partial PATCH)
# ==================================================
separator("6. UserUpdate — Partial update model")
update = UserUpdate(email="new@email.com")  # Only updating email
print(update.model_dump(exclude_none=True))

# ==================================================
# 7. PAYMENT — Cross-field & Luhn validation
# ==================================================
separator("7. PaymentCreate — Expired card (should fail)")
try:
    PaymentCreate(
        card_number="4532015112830366",
        expiry_month=1,
        expiry_year=2022,  # expired
        cvv="123",
        amount=999.0
    )
except ValidationError as e:
    for err in e.errors():
        print(f"  Error: {err['msg']}")

separator("7b. PaymentCreate — Valid card")
pay = PaymentCreate(
    card_number="4532015112830366",
    expiry_month=12,
    expiry_year=2028,
    cvv="123",
    amount=1499.0,
    currency="INR"
)
print(f"Payment: ₹{pay.amount} {pay.currency} | Card: ****{pay.card_number[-4:]}")

# ==================================================
# 8. USER RESPONSE — safe output (no password)
# ==================================================
separator("8. UserResponse — No password in output")
user_resp = UserResponse(
    id=1,
    username="kanishk_sb",
    email="kanishk@example.com",
    age=20,
    role=UserRole.user,
    address=Address(street="12 NIT Campus", city="Surat", zip_code="39500"),
    created_at=datetime.now()
)
resp_dict = user_resp.model_dump()
print("Has password field:", "password" in resp_dict)
print("Fields returned:", list(resp_dict.keys()))

print("\n✅ All demos complete.\n")