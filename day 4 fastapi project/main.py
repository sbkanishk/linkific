from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

# 1. INITIALIZE THE APP
# This creates the central core of our web server application
app = FastAPI(title="Book & User API", version="1.0")


# 2. DEFINE THE DATA RULES (SCHEMAS)
# Pydantic makes sure users send the correct data types (numbers vs strings)
class Book(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    price: float

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    price: Optional[float] = None

class User(BaseModel):
    id: int
    username: str
    email: str
    age: int

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None


# 3. IN-MEMORY FAKE DATABASES
# Instead of a heavy real database, we use simple Python dictionaries to hold data while running
books_db = {}
users_db = {}


# --- HOMEPAGE ROUTE ---
@app.get("/")
def home():
    return {"message": "Welcome! Go to http://127.0.0.1:8000/docs to see the magic interactive page! 🚀"}


# ==========================================
# 4. BOOKS CRUD ENDPOINTS
# ==========================================

# CREATE a book
@app.post("/books/", status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    if book.id in books_db:
        raise HTTPException(status_code=400, detail="Book with this ID already exists.")
    books_db[book.id] = book.dict()
    return books_db[book.id]

# READ ALL books (with search & pagination filters)
@app.get("/books/", status_code=status.HTTP_200_OK)
def get_books(author: Optional[str] = None, skip: int = 0, limit: int = 10):
    results = list(books_db.values())
    if author:
        results = [b for b in results if author.lower() in b['author'].lower()]
    return results[skip : skip + limit]

# READ ONE specific book
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
def get_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found 👀")
    return books_db[book_id]

# UPDATE a whole book (Replace it)
@app.put("/books/{book_id}", status_code=status.HTTP_200_OK)
def update_book(book_id: int, updated_book: Book):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found 👀")
    books_db[book_id] = updated_book.dict()
    return books_db[book_id]

# PATCH a book (Update only parts of it)
@app.patch("/books/{book_id}", status_code=status.HTTP_200_OK)
def patch_book(book_id: int, book_update: BookUpdate):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found 👀")
    stored_data = books_db[book_id]
    update_data = book_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        stored_data[key] = value
    books_db[book_id] = stored_data
    return stored_data

# DELETE a book
@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found 👀")
    del books_db[book_id]
    return {"detail": f"Book {book_id} was successfully tossed in the trash! 🗑️"}


# ==========================================
# 5. USERS CRUD ENDPOINTS
# ==========================================

# CREATE a user
@app.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User with this ID already exists.")
    users_db[user.id] = user.dict()
    return users_db[user.id]

# READ ALL users (with filter & pagination)
@app.get("/users/", status_code=status.HTTP_200_OK)
def get_users(username: Optional[str] = None, skip: int = 0, limit: int = 10):
    results = list(users_db.values())
    if username:
        results = [u for u in results if username.lower() in u['username'].lower()]
    return results[skip : skip + limit]

# READ ONE specific user
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found 👀")
    return users_db[user_id]

# UPDATE a whole user
@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, updated_user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found 👀")
    users_db[user_id] = updated_user.dict()
    return users_db[user_id]

# PATCH a user
@app.patch("/users/{user_id}", status_code=status.HTTP_200_OK)
def patch_user(user_id: int, user_update: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found 👀")
    stored_data = users_db[user_id]
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        stored_data[key] = value
    users_db[user_id] = stored_data
    return stored_data

# DELETE a user
@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found 👀")
    del users_db[user_id]
    return {"detail": f"User {user_id} removed! 👋"}