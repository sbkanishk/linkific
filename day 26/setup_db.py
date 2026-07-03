import sqlite3
import random
import time

def init_sandbox():
    print("🚀 Initializing sandbox database...")
    # Connects to a local SQLite database file in the same folder
    conn = sqlite3.connect("performance.db")
    cursor = conn.cursor()

    # Drop tables if they already exist to keep it clean
    cursor.execute("DROP TABLE IF EXISTS posts;")
    cursor.execute("DROP TABLE IF EXISTS users;")

    # Create tables WITHOUT any explicit indexes for now
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        views INTEGER NOT NULL,
        user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)
    
    conn.commit()

    # Seed 1,000 dummy users
    print("👥 Seeding 1,000 users...")
    users_data = [(f"User_{i}", f"user{i}@example.com") for i in range(1, 1001)]
    cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?);", users_data)
    conn.commit()

    # Seed 50,000 dummy posts distributed randomly across those users
    print("📝 Seeding 50,000 posts (this might take a few seconds)...")
    posts_data = []
    for i in range(1, 50001):
        title = f"Post Title Number {i}"
        content = f"This is the detailed markdown text body for sample blog post article number {i}."
        views = random.randint(0, 10000)
        user_id = random.randint(1, 1000) # randomly assign to a user id between 1 and 1000
        posts_data.append((title, content, views, user_id))
        
    cursor.executemany("INSERT INTO posts (title, content, views, user_id) VALUES (?, ?, ?, ?);", posts_data)
    conn.commit()
    
    # Close connection
    conn.close()
    print("✅ Sandbox database 'performance.db' created successfully with populated records!")

if __name__ == "__main__":
    start_time = time.time()
    init_sandbox()
    print(f"⏱️ Total setup execution time: {time.time() - start_time:.2f} seconds")