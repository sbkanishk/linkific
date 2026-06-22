# Day 16: Authentication & User Management API Documentation

This project implements a secure, state-of-the-art authentication and authorization layer using **Django REST Framework (DRF)** and **JSON Web Tokens (JWT)** via `djangorestframework-simplejwt`.

---

## 🔐 Authentication Architecture Flow

The system uses short-lived **Access Tokens** (5-minute expiration) to secure data endpoints and long-lived **Refresh Tokens** to renew access without forcing users to re-enter credentials.

1. **User Registration:** Guests submit account details; passwords are automatically hashed using PBKDF2 before database storage.
2. **Token Generation (Login):** Valid credentials return both `access` and `refresh` token strings.
3. **Protected Requests:** The client attaches the access token to the HTTP request header:
   `Authorization: Bearer <your_access_token>`
4. **Token Refreshing:** Expired access tokens (`401 Unauthorized`) are seamlessly renewed using the refresh token endpoint.

---

## 🚀 API Endpoint Reference

### 1. User Authentication & Registration

| Endpoint | Method | Access | Description | Payload (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| `/api/users/register/` | **POST** | Public | Create a new user account | `{"username": "...", "email": "...", "password": "..."}` |
| `/api/token/` | **POST** | Public | Login & obtain JWT token pair | `{"username": "...", "password": "..."}` |
| `/api/token/refresh/` | **POST** | Public | Renew an expired access token | `{"refresh": "<your_refresh_token>"}` |

### 2. User Profile Management

| Endpoint | Method | Access | Description |
| :--- | :--- | :--- | :--- |
| `/api/users/profile/` | **GET** | Authenticated | Retrieve current logged-in user profile |
| `/api/users/profile/` | **PUT / PATCH** | Authenticated | Update profile details (`first_name`, `last_name`, `email`) |
| `/api/users/change-password/` | **POST** | Authenticated | Change user password safely |

### 3. Blog Application Permissions

| Endpoint | Method | Allowed Roles | Permission Logic |
| :--- | :--- | :--- | :--- |
| `/blog/posts/` | **GET** | Public | Anyone can view the list of posts (`ReadOnly`) |
| `/blog/posts/` | **POST** | Authenticated | Any logged-in user can create a post |
| `/blog/posts/<id>/` | **PUT / PATCH / DELETE** | Post Owner | Only the specific author who created the post can modify or delete it |

---

## 🛠️ Handling Common Authentication Errors

During API testing in Postman, you might encounter these standard defensive responses:

* **`401 Unauthorized` (token_not_valid):** The access token has expired. Send your refresh token to `/api/token/refresh/` to acquire a new one.
* **`401 Unauthorized` (bad_authorization_header):** The header is malformed. Ensure your Postman type is set to **Bearer Token** and contains no accidental white spaces or newlines.
* **`403 Forbidden`:** You are authenticated but do not own the object you are trying to change (`IsOwnerOrReadOnly` protection triggered).