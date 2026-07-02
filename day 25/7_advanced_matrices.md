# 📊 Advanced Comparisons, Patterns & Architectural Details

## 1. Fine-Grained API Design & Status Codes
To ensure client applications can gracefully handle responses, standard HTTP status codes must be explicitly applied:

### Core Status Codes:
* `200 OK` -> Request succeeded with a return payload.
* `201 Created` -> Resource successfully created (e.g., after a `POST` request).
* `400 Bad Request` -> Client-side payload validation failed.
* `401 Unauthorized` -> Missing or invalid authentication token.
* `403 Forbidden` -> Authenticated client lacks permission for the specific resource.
* `404 Not Found` -> The targeted resource path does not exist.
* `500 Internal Server Error` -> Generic unhandled server-side crash.

### Advanced Concepts:
* **Filtering & Sorting:** Handled via query parameters: `GET /products?category=shoes&sort=-price,name` (where `-` indicates descending order).
* **API Versioning:** Can be managed via the URL (`/v1/users`) or via request headers (`Accept: application/vnd.company.v1+json`).
* **HATEOAS (Hypermedia As The Engine Of Application State):** A REST architecture principle where the server returns data along with hyperlinks directing the client to all related actions they can take next from that state.

---

## 2. Technology Comparison Matrices

### Database Selection: SQL vs. NoSQL
| Metric | Relational (SQL) | Non-Relational (NoSQL) |
| :--- | :--- | :--- |
| **Schema** | Rigid, predefined structure. | Flexible, dynamic schemas (Document, Key-Value). |
| **Scaling** | Vertical (scale up hardware). | Horizontal (scale out across machines). |
| **Transactions** | Strict ACID compliance. | BASE properties (Eventual consistency). |
| **Best Case** | Financial ledger, Order service. | Live tracking coordinates, User carts. |

### Authentication Strategies
| Method | Storage / Mechanism | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **Session-Based** | Server-side memory/Redis + Cookie. | Revocable instantly by the server. | Requires stateful server scaling. |
| **JWT (Tokens)** | Client-side storage (HttpOnly). | Stateless, highly scalable. | Cannot be easily revoked before expiration. |
| **OAuth 2.0** | Delegation protocol via Auth server. | Secure third-party access limits. | Complex architecture setup. |

---

## 3. Operations: Alerting & Penetration Testing

### Alerting Strategies
* **Symptom-Based Alerting:** Focus on alerting based on user-facing symptoms (e.g., HTTP 5xx spikes or high p99 latency) rather than trying to alert on every single minor CPU spike.
* **Dead Man's Snitch:** Implement heartbeats for background cron jobs to immediately flag when an automated operational script silently fails to execute.

### Penetration Testing Basics
* **Black Box Testing:** Simulating an external cyberattack where the tester has zero prior knowledge of the underlying system architecture or codebase.
* **White Box Testing:** Full-transparency analysis where security engineers review the source code, API blueprints, and internal configurations to find deep-seated logic flaws.