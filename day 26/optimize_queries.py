import sqlite3
import time

def apply_optimizations():
    conn = sqlite3.connect("performance.db")
    cursor = conn.cursor()

    print("⚡ Creating indexes...")
    # 1. Create B-Tree index on users(email)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
    # 2. Create index on posts(views) for range scans
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_views ON posts(views);")
    conn.commit()
    print("✅ Indexes created successfully!\n")

    print("--- 🚀 TEST 1: Indexed Column Lookups (Exact Match) ---")
    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'user500@example.com';")
    print("New Execution Plan:", cursor.fetchone()[3])
    
    start = time.perf_counter()
    for _ in range(200):
        cursor.execute("SELECT * FROM users WHERE email = 'user500@example.com';")
        cursor.fetchall()
    print(f"⏱️ Time taken for 200 lookups: {(time.perf_counter() - start) * 1000:.2f} ms")


    print("\n--- 🚀 TEST 2: Indexed High View Count Search ---")
    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM posts WHERE views > 9500;")
    print("New Execution Plan:", cursor.fetchone()[3])
    
    start = time.perf_counter()
    cursor.execute("SELECT * FROM posts WHERE views > 9500;")
    results = cursor.fetchall()
    print(f"⏱️ Time taken to find popular posts: {(time.perf_counter() - start) * 1000:.2f} ms")


    print("\n--- 🚀 TEST 3: Fixing N+1 Using an Inner JOIN ---")
    cursor.execute("EXPLAIN QUERY PLAN SELECT p.id, p.title, u.name FROM posts p JOIN users u ON p.user_id = u.id LIMIT 100;")
    print("JOIN Execution Plan:", cursor.fetchone()[3])
    
    start = time.perf_counter()
    # Fetch all data in exactly 1 database query instead of 101 queries!
    cursor.execute("""
        SELECT p.id, p.title, u.name 
        FROM posts p 
        JOIN users u ON p.user_id = u.id 
        LIMIT 100;
    """)
    results = cursor.fetchall()
    print(f"⏱️ Time taken for clean JOIN (100 posts): {(time.perf_counter() - start) * 1000:.2f} ms")

    conn.close()

if __name__ == "__main__":
    apply_optimizations()