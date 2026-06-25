# FastAPI Caching System with Redis 🚀

This project implements a high-performance caching layer for a FastAPI application using Redis and Docker Compose.

## 🛠️ Tech Stack
* **Framework:** FastAPI
* **Cache Store:** Redis (7-alpine)
* **Orchestration:** Docker Compose

## 💡 Caching Strategy

### 1. Cache-Aside Pattern
The application uses the classic Cache-Aside approach for reading data:
* Check Redis first for the requested data.
* **Cache Hit:** Return data instantly from Redis memory.
* **Cache Miss:** Query the source (database simulation), save it to Redis with a TTL, and return.

### 2. Custom Caching Decorator (`@cache`)
A reusable `@cache(ttl=X)` python decorator was built to automate caching across any endpoint. It dynamically constructs unique cache keys using the syntax:
`function_name:param1=value1,param2=value2`

### 3. Cache Invalidation
To prevent stale data, any data mutation (`PUT` request) actively destroys the specific Redis cache key using `r.delete(cache_key)`. This guarantees the next read operation pulls fresh data.

## 🚀 How to Run

1. Open a terminal in the project directory.
2. Spin up the entire multi-container ecosystem:
   ```bash
   docker compose up --build

   http://127.0.0.1:8000/users/101