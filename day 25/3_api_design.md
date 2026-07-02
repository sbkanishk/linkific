# 🎨 API Design Best Practices & Alternative Styles

## 1. RESTful Resource Naming & HTTP Methods
An elegant API uses plural nouns for resources, keeping the URLs clean. The actual action is determined entirely by the HTTP method used.

* **Good Practice:** `GET /users/42` (Fetches user details)
* **Bad Practice:** `POST /getUserDetails/42` (Uses verbs and leaks implementation details)

### HTTP Methods Mapping:
* `GET` -> Read a resource (Safe and idempotent).
* `POST` -> Create a new resource (Non-idempotent).
* `PUT` -> Replace an entire resource.
* `PATCH` -> Partially update an existing resource.
* `DELETE` -> Remove a resource.

---

## 2. Pagination Strategies: Offset vs. Cursor

### Offset Pagination (`?page=3&limit=20`)
* **How it works:** Uses `LIMIT` and `OFFSET` in SQL to skip rows.
* **Pros:** Extremely simple to implement; allows users to jump directly to specific page numbers.
* **Cons:** Becomes highly inefficient ($O(N)$ time complexity) on deep pages because the database must scan through all skipped rows. It can also cause duplicate or skipped items if data is added or removed while scrolling.

### Cursor Pagination (`?after=user_id_99&limit=20`)
* **How it works:** Uses a pointer (like a unique ID or timestamp) to fetch rows *after* the last seen record.
* **Pros:** Highly performant ($O(1)$ constant time complexity) because it relies on database indexes. It completely prevents data shifting or duplicates during real-time scrolling.
* **Cons:** Does not allow users to jump directly to an arbitrary page number (e.g., page 45).
* **Best For:** Infinite scrolling feeds (like Instagram, Twitter, or complex activity logs).

---

## 3. Alternative API Styles & Protocols

### GraphQL
* **Core Idea:** A single endpoint where the client sends a query specifying the exact fields it needs.
* **When to use:** Complex frontend layouts with highly nested data structures, where standard REST would lead to excessive over-fetching or multiple network round trips.

### gRPC
* **Core Idea:** High-performance, low-latency framework utilizing HTTP/2 and binary Protocol Buffers instead of text-based JSON.
* **When to use:** Strictly for low-latency, internal microservice-to-microservice communication where serialization speed is vital.

### WebSockets vs. Server-Sent Events (SSE)
* **WebSockets:** Full-duplex, persistent two-way communication channel between client and server. Best for bidirectional real-time features like chat applications or collaborative whiteboards.
* **Server-Sent Events (SSE):** Lightweight, unidirectional one-way communication channel where the server streams updates to the client over standard HTTP. Best for real-time dashboards, live stock tickers, or push notifications.