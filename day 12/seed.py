from app.database import SessionLocal, engine, Base
from app.models import User, Category, Product
from app.auth import hash_password

def seed_database():
    print("Initializing database tables...")
    Base.metadata.drop_all(bind=engine) # Resets data cleanly for a fresh run
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("Seeding default administrative and customer users...")
        admin = User(username="admin", email="admin@shop.com", hashed_password=hash_password("admin123"), role="admin")
        customer = User(username="customer", email="buyer@shop.com", hashed_password=hash_password("buyer123"), role="customer")
        db.add_all([admin, customer])
        db.commit()

        print("Seeding sample industrial categories...")
        electronics = Category(name="Electronics", description="High-tech gadgets and devices")
        apparel = Category(name="Apparel", description="Clothing and fine fabrics")
        books = Category(name="Books", description="Knowledge and literary scrolls")
        db.add_all([electronics, apparel, books])
        db.commit()

        print("Seeding market products...")
        p1 = Product(name="Quantum Laptop", description="Blazing fast calculations", price=1299.99, stock=15, image_url="https://images.com/laptop.png", category_id=electronics.id)
        p2 = Product(name="Cyber Phone", description="Sleek pocket communicator", price=799.50, stock=45, image_url="https://images.com/phone.png", category_id=electronics.id)
        p3 = Product(name="Leather Jacket", description="Classic stylish armor", price=180.00, stock=20, image_url="https://images.com/jacket.png", category_id=apparel.id)
        p4 = Product(name="Python Codex", description="Mastering the syntax arrays", price=45.00, stock=120, image_url="https://images.com/book.png", category_id=books.id)
        
        db.add_all([p1, p2, p3, p4])
        db.commit()
        print("Database successfully seeded with fresh testing records! 🎉")
        
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()