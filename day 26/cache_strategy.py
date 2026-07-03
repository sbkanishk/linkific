import sqlite3
import time

# Our simulated in-memory cache (like Redis)
user_cache = {}

def get_user_email_db(cursor, user_id):
    """Fetches user email directly from the database."""
    cursor.execute("SELECT email FROM users WHERE id = ?;", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_user_email_with_cache(cursor, user_id):
    """Fetches user email using the Cache-Aside strategy."""
    # 1. Check the cache first (Cache Hit)
    if user_id in user_cache:
        return user_cache[user_id], "HIT"
    
    # 2. If not found, fetch from database (Cache Miss)
    cursor.execute("SELECT email FROM users WHERE id = ?;", (user_id,))
    result = cursor.fetchone()
    email = result[0] if result else None
    
    # 3. Save to cache for future requests
    if email:
        user_cache[user_id] = email
        
    return email, "MISS"

def run_cache_demo():
    conn = sqlite3.connect("performance.db")
    cursor = conn.cursor()
    
    target_user_id = 742
    
    print("--- 📦 Run 1: Direct Database Request (No Caching) ---")
    start = time.perf_counter()
    for _ in range(500):
        get_user_email_db(cursor, target_user_id)
    print(f"⏱️ Time taken for 500 DB lookups: {(time.perf_counter() - start) * 1000:.2f} ms")
    
    print("\n--- 📦 Run 2: Cache-Aside Implementation ---")
    # First request: Cache Miss (goes to DB)
    email, status = get_user_email_with_cache(cursor, target_user_id)
    print(f"1st Request Status: {status} (Email: {email})")
    
    # Next 500 requests: Cache Hits (instant)
    start = time.perf_counter()
    for _ in range(500):
        get_user_email_with_cache(cursor, target_user_id)
    print(f"⏱️ Time taken for 500 Cached lookups: {(time.perf_counter() - start) * 1000:.2f} ms")
    
    conn.close()

if __name__ == "__main__":
    run_cache_demo()