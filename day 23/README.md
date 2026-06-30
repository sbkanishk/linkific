# Day 23: Backend Algorithmic Optimizations 🚀

This module demonstrates core algorithmic implementations optimized specifically for production backend scenarios using Python and FastAPI.

---

## ⏱️ Big O Matrix & Complexity Profiles

| Algorithm | Time Complexity | Space Complexity | Real-World Backend Application |
| :--- | :--- | :--- | :--- |
| **Linear Search** | $O(n)$ | $O(1)$ | Scanning un-indexed, raw data payloads. |
| **Binary Search** | $O(\log n)$ | $O(1)$ | Blazing fast row lookup via indexed unique IDs. |
| **Bubble Sort** | $O(n^2)$ | $O(1)$ | Educational only. Avoid completely in high-throughput routes. |
| **Quick Sort** | $O(n \log n)$ | $O(\log n)$ | Efficiently organizing bulk reporting logs. |
| **Merge Sort** | $O(n \log n)$ | $O(n)$ | Stable sorting where order parity of match records matters. |
| **Two Pointers** | $O(n)$ | $O(1)$ | Eliminating nested query filters for target matches. |
| **Sliding Window** | $O(n)$ | $O(n)$ | Enforcing precise, memory-conscious API rate limiting. |
| **BFS (Graph)** | $O(V + E)$ | $O(V)$ | Discovering shortest-path user connection paths ("degrees of separation"). |
| **DFS (Graph)** | $O(V + E)$ | $O(V)$ | Resolving deep dependency graphs or multi-level category trees. |

---

## 🛠️ Verifying API Endpoints

Once your server is active via `python -m uvicorn app:app --reload`, open your browser or postman client and hit these endpoints:

1. **Optimized Lookup:** `GET http://127.0.0.1:8000/products/4322`
2. **Graph Connection Paths:** `GET http://127.0.0.1:8000/network/shortest-path?start=Shashi&target=Shubham`
3. **Log Sorters:** `GET http://127.0.0.1:8000/orders/sorted`

*Note: Repeatedly spamming the product route will exhaust capacity and trigger the active **Sliding Window Rate Limiter** with an HTTP 429 restriction block.*

python -m uvicorn app:app --reload