## 🚀 Day 15: Building the REST APIs

Upgraded the application architecture by integrating the **Django REST Framework (DRF)**. Transitioned from standard HTML templates to returning raw, formatted JSON data, preparing the backend to serve frontend frameworks (like React) or mobile applications.

### 🛠️ Key Technical Implementations:
* **Serializers:** Built complex translation layers (`ModelSerializer`) to convert SQLite database models into JSON format.
* **ViewSets:** Swapped standard Django Views for DRF `ModelViewSets`, automatically generating complete CRUD (Create, Read, Update, Delete) operations with minimal code.
* **Routers:** Implemented DRF `DefaultRouter` to automatically generate standard API URL endpoints (`/store/products/`, `/blog/posts/`, etc.).
* **Pagination & Filtering:** Configured global pagination and integrated `django_filters` for advanced searching and ordering capabilities directly from the URL parameters.
* **Multi-App Architecture:** Successfully scaled the API across two independent Django apps (`store` and `blog`).
* **API Testing:** Built and tested endpoints using Postman to verify HTTP status codes (`200 OK`, `201 Created`).