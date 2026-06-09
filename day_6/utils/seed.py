import sys
import os

# Adjusting path to make sure Python can find our database/config files smoothly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection_orm import SessionLocal, engine, Base
from database import models

def seed_database():
    print("Dropping old database tables if they exist...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creating clean, fresh tables from our models...")
    Base.metadata.create_all(bind=engine)
    
    # Spin up a localized database session
    db = SessionLocal()
    try:
        print("Injecting sample user records...")
        user1 = models.User(username="alice_dev", email="alice@example.com")
        user2 = models.User(username="bob_test", email="bob@example.com")
        db.add_all([user1, user2])
        db.commit() # Commit changes to database so they generate valid auto-incrementing IDs
        
        print("Injecting sample item records linked to our users...")
        item1 = models.Item(title="Mechanical Keyboard", description="RGB Blue Switches", price=8500, owner_id=user1.id)
        item2 = models.Item(title="Ergonomic Mouse", description="Wireless 2.4Ghz vertical mouse", price=4500, owner_id=user1.id)
        item3 = models.Item(title="4K Monitor", description="UltraWide IPS Panel", price=32000, owner_id=user2.id)
        
        db.add_all([item1, item2, item3])
        db.commit()
        print("🎉 Database seeded successfully with test records!")
        
    except Exception as e:
        db.rollback() # Rollback transaction if anything fails mid-process
        print(f"❌ Seeding failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
    