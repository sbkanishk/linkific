from typing import Optional
from security import hash_password

fake_users_db: dict[str, dict] = {
    "admin": {
        "username": "admin",
        "email": "admin@linkific.com",
        "hashed_password": hash_password("admin123"),
        "role": "admin",
        "disabled": False,
    },
    "kanishk": {
        "username": "kanishk",
        "email": "kanishk@linkific.com",
        "hashed_password": hash_password("pass123"),
        "role": "user",
        "disabled": False,
    },
}

def get_user(username: str) -> Optional[dict]:
    return fake_users_db.get(username)

def get_user_by_email(email: str) -> Optional[dict]:
    for user in fake_users_db.values():
        if user["email"] == email:
            return user
    return None

def create_user(username: str, email: str, password: str, role: str = "user") -> dict:
    if username in fake_users_db:
        raise ValueError(f"Username '{username}' already exists.")
    if get_user_by_email(email):
        raise ValueError(f"Email '{email}' is already registered.")

    user = {
        "username": username,
        "email": email,
        "hashed_password": hash_password(password),
        "role": role,
        "disabled": False,
    }
    fake_users_db[username] = user
    return user

def list_users() -> list[dict]:
    return [
        {k: v for k, v in u.items() if k != "hashed_password"}
        for u in fake_users_db.values()
    ]