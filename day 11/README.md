# Day 11: E-Commerce Backend Architecture

## Project Overview
This project sets up the foundational workspace, database schema, and API endpoint design for a full-scale e-commerce application using FastAPI.

## Folder Structure
- `auth/`: Handles user authentication and tokens.
- `database/`: Contains database connection scripts and database schemas.
- `models/`: Database ORM models (SQLAlchemy).
- `routers/`: API route definitions split by module.
- `schemas/`: Data validation and serialization schemas (Pydantic).
- `utils/`: Helper scripts and utility functions.

## API Specification Matrix

| Module | Method | Endpoint | Access Level | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Auth** | `POST` | `/register` | Public | Register a new user account |
| | `POST` | `/login` | Public | Authenticate user and return token |
| **Products** | `GET` | `/products` | Public | List all available products |
| | `POST` | `/products` | Admin Only | Create a new product entry |
| | `GET` | `/products/{id}` | Public | Fetch specific product details |
| | `PUT` | `/products/{id}` | Admin Only | Update an existing product |
| | `DELETE`| `/products/{id}` | Admin Only | Remove a product from inventory |
| **Categories**| `GET` | `/categories` | Public | List all product categories |
| | `POST` | `/categories` | Admin Only | Create a new category |
| **Cart** | `GET` | `/cart` | Customer | View items currently in the cart |
| | `POST` | `/cart/items` | Customer | Add or update an item in the cart |
| | `DELETE`| `/cart/items/{id}`| Customer | Remove an item from the cart |
| **Orders** | `POST` | `/orders` | Customer | Checkout and place an order |
| | `GET` | `/orders` | Mixed | View order history |
| **Reviews** | `POST` | `/products/{id}/reviews`| Customer | Submit a product review |
| **Search** | `GET` | `/products/search`| Public | Search products by text keyword |