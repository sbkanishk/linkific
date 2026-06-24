from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database

app = FastAPI(title="Task Manager API")

# Create database tables automatically on startup
models.Base.metadata.create_all(bind=database.engine)

# Super simple mock hashing for speed/comparison parity
def fake_hash_password(password: str):
    return password + "notreallyhashed"

@app.post("/auth/register/", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pass = fake_hash_password(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/tasks/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, user_id: int, db: Session = Depends(database.get_db)):
    new_task = models.Task(**task.model_dump(), owner_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks/", response_model=List[schemas.TaskResponse])
def get_tasks(user_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()