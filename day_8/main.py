import os
import time
from typing import Dict, Any
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
import jwt # PyJWT package
from config import settings

app = FastAPI(title="Linkific OAuth Service - Day 8 Complete")

# Required by Authlib to maintain secure state parameters across redirects
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Allow OAuth callback to work over HTTP during local development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# In-Memory Database Simulation for OAuth Users
# In production, this would be your PostgreSQL/SQLAlchemy User table
database_simulation: Dict[str, Dict[str, Any]] = {}

# Initialize and register Google OAuth Client
oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

def create_application_jwt(user_email: str) -> str:
    """
    Generates a secure, signed native JWT from Linkific to send to the frontend.
    """
    payload = {
        "sub": user_email,
        "iss": "linkific-backend",
        "iat": int(time.time()),
        "exp": int(time.time()) + (60 * 60) # Token valid for 1 hour
    }
    # Sign using the same SECRET_KEY from your configuration
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    The secure 'Login with Google' entry portal.
    """
    return """
    <html>
        <head>
            <title>Linkific Auth Hub</title>
            <style>
                body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f7f9fa; margin: 0; }
                .card { padding: 40px; background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-radius: 12px; text-align: center; max-width: 400px; width: 100%; }
                .btn { display: inline-block; padding: 12px 24px; background: #4285F4; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; margin-top: 20px; transition: background 0.2s; }
                .btn:hover { background: #357ae8; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>Welcome to Linkific</h2>
                <p>Secure OAuth 2.0 Integration Workspace</p>
                <a class="btn" href="/auth/login/google">Login with Google</a>
            </div>
        </body>
    </html>
    """

@app.get("/auth/login/google")
async def login_google(request: Request):
    """
    Redirects the user safely to Google's authorization servers.
    """
    redirect_uri = request.url_for('auth_callback_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/callback/google")
async def auth_callback_google(request: Request):
    """
    Handles token exchange, updates database records, and signs a custom app JWT.
    """
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        if not user_info:
            return JSONResponse(status_code=400, content={"error": "Failed to parse profile details from Google."})
            
        email = user_info.get("email")
        google_id = user_info.get("sub")
        name = user_info.get("name")
        picture = user_info.get("picture")
        
        # --- DATABASE UPSERT INTEGRATION LAYER ---
        if email not in database_simulation:
            # First-time user signup flow via OAuth
            database_simulation[email] = {
                "email": email,
                "name": name,
                "google_id": google_id,
                "picture": picture,
                "account_linked": True,
                "created_at": "Just Now (OAuth Generated)"
            }
            auth_action = "Registration via Google successful"
        else:
            # Existing user profile synchronization flow
            database_simulation[email]["name"] = name
            database_simulation[email]["picture"] = picture
            database_simulation[email]["google_id"] = google_id
            auth_action = "Login via Google successful (Profile Synced)"
            
        # --- NATIVE APPLICATION JWT GENERATION ---
        app_jwt = create_application_jwt(email)
        
        return {
            "status": "success",
            "action": auth_action,
            "access_token": app_jwt,
            "token_type": "bearer",
            "user_profile": database_simulation[email]
        }
        
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"OAuth handshake failed: {str(e)}"})