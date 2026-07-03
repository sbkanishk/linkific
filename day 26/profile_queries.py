import sqlite3
import time

def run_profiling():
    conn = sqlite3.connect("performance.db")
    cursor = conn.cursor()

    print("\n--- 🔍 TEST 1: Scanning Unindexed Column (Exact Match) ---")
    # Let's inspect the execution plan using EXPLAIN QUERY PLAN
    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'user500@example.com';")
    print("Execution Plan:", cursor.fetchone()[3])
    
    start = time.perf_counter()
    for _ in range(200):  # Repeat to make the difference noticeable
        cursor.execute("SELECT * FROM users WHERE email = 'user500@example.com';")
        cursor.fetchall()
    print(f"⏱️ Time taken for 200 lookups: {(time.perf_counter() - start) * 1000:.2f} ms")


    print("\n--- 🔍 TEST 2: High View Count Search & Range Scan ---")
    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM posts WHERE views > 9500;")
    print("Execution Plan:", cursor.fetchone()[3])
    
    start = time.perf_counter()
    cursor.execute("SELECT * FROM posts WHERE views > 9500;")
    results = cursor.fetchall()
    print(f"⏱️ Time taken to find popular posts: {(time.perf_counter() - start) * 1000:.2f} ms (Found {len(results)} rows)")


    print("\n--- 🔍 TEST 3: The Evil N+1 Query Demonstration ---")
    start = time.perf_counter()
    
    # 1. Fetch 100 posts (The "1" query)
    cursor.execute("SELECT id, title, user_id FROM posts LIMIT 100;")
    posts = cursor.fetchall()
    
    # 2. For each post, hit the database again to fetch the author name (The "N" queries)
    for post in posts:
        user_id = post[2]
        cursor.execute("SELECT name FROM users WHERE id = ?;", (user_id,))
        cursor.fetchone()
        
    print(f"⏱️ Time taken for N+1 loop (100 posts): {(time.perf_counter() - start) * 1000:.2f} ms")

    conn.close()

if __name__ == "__main__":
    run_profiling()