from pydantic import BaseModel, EmailStr, field_validator
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Role = Role.user

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        return v

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("Username must contain only letters and numbers.")
        return v.lower()

class UserResponse(BaseModel):
    username: str
    email: str
    role: Role
    disabled: bool

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MeResponse(BaseModel):
    username: str
    email: str
    role: str