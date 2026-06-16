import logging
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional

# 1. Setup Structured Logging Configurations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("__main__")

app = FastAPI(title="Linkific Week 1 Complete API")

# Mock Database Store
items_db = []
users_db = {}

# Data Schemas
class UserRegister(BaseModel):
    username: str
    password: str

class Item(BaseModel):
    name: str
    description: str

# 2. Try-Except Error Logging Helper / Dependency
def verify_token(authorization: Optional[str] = Header(None)):
    logger.info("Verifying incoming request authentication token...")
    try:
        if not authorization or not authorization.startswith("Bearer "):
            logger.warning("Authentication failure: Missing or invalid header structure.")
            raise HTTPException(status_code=401, detail="Missing or invalid access token.")
        
        token = authorization.split(" ")[1]
        if token != "linkific_secret_session_token_2026":
            logger.error("Authentication failure: Token mismatch detection.")
            raise HTTPException(status_code=401, detail="Session expired or invalid token.")
        
        logger.info("Authentication token validated successfully!")
        return True
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        logger.critical(f"Unexpected authentication crash: {str(err)}")
        raise HTTPException(status_code=500, detail="Internal server authentication error.")

# --- ENDPOINTS ---

@app.get("/")
def get_root():
    logger.info("Root endpoint hit successfully!")
    return {"message": "Welcome to Day 10 Complete API Suite!"}

@app.post("/auth/register")
def register_user(user: UserRegister):
    logger.info(f"Attempting registration for user: {user.username}")
    if user.username in users_db:
        logger.warning(f"Registration rejected: Username '{user.username}' already exists.")
        raise HTTPException(status_code=400, detail="Username already registered.")
    
    users_db[user.username] = user.password
    logger.info(f"User '{user.username}' successfully registered.")
    return {"message": "Registration successful!"}

@app.post("/auth/login")
def login_user(user: UserRegister):
    logger.info(f"Login attempt received for user: {user.username}")
    if user.username not in users_db or users_db[user.username] != user.password:
        logger.error(f"Failed login attempt for user: {user.username}")
        raise HTTPException(status_code=400, detail="Invalid username or password.")
    
    # Generate static secure token for chaining tasks
    mock_token = "linkific_secret_session_token_2026"
    logger.info(f"User '{user.username}' authenticated successfully. Token dispatched.")
    return {"access_token": mock_token, "token_type": "bearer"}

@app.post("/items/")
def create_item(item: Item, authenticated: bool = Depends(verify_token)):
    logger.info(f"Attempting to create a new item: {item.name}")
    
    if item.name.lower() == "error":
        logger.error("An intentional database validation error was triggered by the user!")
        raise HTTPException(status_code=400, detail="Item name cannot be 'error'")
        
    items_db.append(item.dict())
    logger.info(f"Item '{item.name}' successfully added to database.")
    return {"message": "Item created", "data": item}