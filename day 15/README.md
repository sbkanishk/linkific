## 🚀 Day 15: Building the REST APIs

Upgraded the application architecture by integrating the **Django REST Framework (DRF)**. Transitioned from standard HTML templates to returning raw, formatted JSON data, preparing the backend to serve frontend frameworks (like React) or mobile applications.

### 🛠️ Key Technical Implementations:
* **Serializers:** Built complex translation layers (`ModelSerializer`) to convert SQLite database models into JSON format.
* **ViewSets:** Swapped standard Django Views for DRF `ModelViewSets`, automatically generating complete CRUD (Create, Read, Update, Delete) operations with minimal code.
* **Routers:** Implemented DRF `DefaultRouter` to automatically generate standard API URL endpoints (`/store/products/`, `/blog/posts/`, etc.).
* **Pagination & Filtering:** Configured global pagination and integrated `django_filters` for advanced searching and ordering capabilities directly from the URL parameters.
* **Multi-App Architecture:** Successfully scaled the API across two independent Django apps (`store` and `blog`).
* **API Testing:** Built and tested endpoints using Postman to verify HTTP status codes (`200 OK`, `201 Created`).

🔗 . Store API Endpoints
Once the server is running, you can click or copy these links directly into your browser or Postman to view and interact with the JSON data:

Products: http://127.0.0.1:8000/store/products/

Categories: http://127.0.0.1:8000/store/categories/

Orders: http://127.0.0.1:8000/store/orders/

Carts: http://127.0.0.1:8000/store/carts/

Reviews: http://127.0.0.1:8000/store/reviews/

🔗 . Blog API Endpoints
Authors: http://127.0.0.1:8000/blog/authors/

Posts: http://127.0.0.1:8000/blog/posts/

Comments: http://127.0.0.1:8000/blog/comments/

python manage.py runserver