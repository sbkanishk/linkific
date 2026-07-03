# 🚀 Day 26: System Scaling Strategy & Architecture Notes

## 1. Vertical vs. Horizontal Scaling
* **Vertical Scaling (Scale Up):** Adding more CPU, RAM, or SSD storage to your existing server.
    * *Pros:* Simple; no code changes required.
    * *Cons:* Has a hard hardware ceiling and creates a Single Point of Failure (SPOF).
* **Horizontal Scaling (Scale Out):** Adding more machines to your cluster (e.g., running 5 smaller servers instead of 1 giant server).
    * *Pros:* Practically infinite scaling potential and high availability.
    * *Cons:* Requires a Load Balancer and architectural complexity.

---

## 2. Load Balancing Strategies
When traffic hits your horizontally scaled servers, a Load Balancer (like Nginx or AWS ALB) routes incoming requests using different strategies:
* **Round Robin:** Requests are distributed sequentially across the server pool (Server 1, then Server 2, then Server 3).
* **Least Connections:** Routes traffic to the server currently handling the fewest active requests.
* **Sticky Sessions (Session Affinity):** Ensures a specific user's requests always hit the exact same backend server. 
    * *Warning:* Avoid sticky sessions if possible by storing user sessions in a centralized Redis cache instead of local server memory!

---

## 3. Database Scaling: Replication vs. Sharding
When the database becomes the ultimate bottleneck:

### A. Database Replication (Master-Slave Architecture)
* **How it works:** You have one **Master DB** and multiple **Slave DBs**.
* **Writes:** All `INSERT`, `UPDATE`, and `DELETE` queries go exclusively to the Master DB.
* **Reads:** All `SELECT` queries are spread across the Slave DBs.
* **Best for:** Read-heavy applications (like blogs, social media, or e-commerce browsing).

### B. Database Sharding (Horizontal Partitioning)
* **How it works:** Breaking a massive table into smaller, manageable chunks across completely separate database servers.
* **Example:** * Users with IDs `1` to `500,000` go to **Database Shard A**.
    * Users with IDs `500,001` to `1,000,000` go to **Database Shard B**.
* **Best for:** Massive write-heavy applications where a single database disk cannot keep up.

---

## 4. Edge Optimization: Content Delivery Networks (CDNs)
* **What it does:** Cached copies of your static assets (HTML, CSS, JS, Images, Videos) are distributed to edge servers worldwide.
* **Why it matters:** Instead of a user in New York hitting your backend server in India for a static logo image, they fetch it instantly from a local New York CDN edge server, reducing server load and network latency.