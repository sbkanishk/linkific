from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Task Schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    is_completed: bool
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True