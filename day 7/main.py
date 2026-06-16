from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from security import verify_password, create_access_token
from database import get_user, create_user, list_users
from schemas import RegisterRequest, UserResponse, TokenResponse, MeResponse
from dependencies import get_current_user, require_role

app = FastAPI(
    title="Linkific Auth API",
    version="1.0.0",
)

@app.post("/auth/register", response_model=UserResponse, status_code=201)
def register(body: RegisterRequest):
    try:
        user = create_user(
            username=body.username,
            email=body.email,
            password=body.password,
            role=body.role.value,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return UserResponse(**{k: v for k, v in user.items() if k != "hashed_password"})


@app.post("/auth/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return TokenResponse(access_token=token)


@app.get("/auth/me", response_model=MeResponse)
def get_me(current_user: dict = Depends(get_current_user)):
    return MeResponse(
        username=current_user["username"],
        email=current_user["email"],
        role=current_user["role"],
    )


@app.get("/users/")
def get_all_users(current_user: dict = Depends(require_role("admin"))):
    return {"users": list_users()}


@app.get("/protected/dashboard")
def dashboard(current_user: dict = Depends(get_current_user)):
    return {"message": f"Welcome, {current_user['username']}!", "role": current_user["role"]}


@app.get("/protected/admin")
def admin_panel(current_user: dict = Depends(require_role("admin"))):
    return {"message": "Admin access granted.", "user": current_user["username"]}


@app.get("/protected/moderator")
def moderator_panel(current_user: dict = Depends(require_role("admin", "moderator"))):
    return {"message": "Moderator access granted.", "user": current_user["username"]}


@app.get("/")
def root():
    return {"message": "Linkific Auth API is live. Visit /docs"}