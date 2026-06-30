from fastapi import FastAPI, HTTPException, Depends
from algorithms import (
    binary_search, 
    quick_sort, 
    bfs_shortest_path, 
    SlidingWindowRateLimiter
)

app = FastAPI(title="Day 23: Algorithmic Backend Optimization API")

# Mock Database Store
PRODUCTS = [{"id": i, "name": f"Product_{i}", "price": 10.0 + (i % 5)} for i in range(1, 10001)]
# Note: PRODUCTS is already naturally sorted by 'id' from 1 to 10000

USER_CONNECTIONS = {
    "Shashi": ["Hemang", "Aman"],
    "Hemang": ["Shashi", "Shubham", "Nitin"],
    "Aman": ["Shashi", "Nitin"],
    "Shubham": ["Hemang"],
    "Nitin": ["Hemang", "Aman"]
}

# Instantiate a global rate limiter: Max 5 requests per 10 seconds
limiter = SlidingWindowRateLimiter(max_requests=5, window_seconds=10)


# Dependable rule to enforce sliding window rate limiting
def check_rate_limit():
    if not limiter.is_allowed():
        raise HTTPException(status_code=429, detail="Too Many Requests - Sliding Window Full! 🛑")


# Endpoints
@app.get("/products/{product_id}", dependencies=[Depends(check_rate_limit)])
def get_product(product_id: int):
    """
    Optimized Product Lookup using Binary Search - O(log n)
    """
    # Extract IDs to feed to our binary search function
    product_ids = [p["id"] for p in PRODUCTS]
    index = binary_search(product_ids, product_id)
    
    if index == -1:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"status": "success", "data": PRODUCTS[index], "method": "Binary Search O(log n)"}


@app.get("/network/shortest-path")
def get_shortest_connection(start: str, target: str):
    """
    Finds the shortest degree of separation between users using BFS - O(V + E)
    """
    path = bfs_shortest_path(USER_CONNECTIONS, start, target)
    if not path:
        raise HTTPException(status_code=404, detail="No connection path found")
    return {"start": start, "target": target, "hops": len(path) - 1, "connection_path": path}


@app.get("/orders/sorted")
def get_sorted_orders():
    """
    Sorts unorganized order logs using Quick Sort - O(n log n)
    """
    raw_order_ids = [64, 34, 25, 12, 22, 11, 90]
    sorted_ids = quick_sort(raw_order_ids)
    return {"original_order_logs": raw_order_ids, "sorted_order_logs": sorted_ids}

import time

# 8.2 Sliding Window Rate Limiter Class for Backend Integration
