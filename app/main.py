from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx, os, jwt
from dotenv import load_dotenv
from urllib.parse import urlencode
from typing import Dict
from app.services.github_service import GithubAuthService
from app.services.google_service import GoogleAuthService

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:4200")
JWT_SECRET = os.getenv("JWT_SECRET", "mysecret")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


github_service = GithubAuthService()    
google_service = GoogleAuthService()

@app.get("/auth/login")
async def login():
    return {"auth_url": github_service.get_auth_url()}

@app.get("/auth/callback")
async def auth_callback(code: str):
    access_token = await github_service.exchange_code_for_token(code)
    if not access_token:
        raise HTTPException(status_code=400, detail="Token exchange failed")
    user = await github_service.get_user(access_token)
    payload = {"sub": user["login"], "id": user["id"]}
    print(payload, "Main-----------------")
    token = github_service.create_jwt(payload)
    print(token, "Main-----------------")
    redirect_url = f"{FRONTEND_URL}/callback?token={token}"
    return RedirectResponse(url=redirect_url)

@app.get("/api/profile")
async def profile(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    token = auth_header.replace("Bearer ", "")
    try:
        user = github_service.decode_jwt(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": "Profile fetched", "user": user}

@app.get("/auth/google/login")
def google_login():
    return {"auth_url": google_service.get_auth_url()}

@app.get("/auth/google/callback")
async def google_callback(code: str):
    access_token = await google_service.exchange_code_for_token(code)
    if not access_token:
        raise HTTPException(status_code=400, detail="Token exchange failed")
    user = await google_service.get_user(access_token)
    payload = {"sub": user["id"], "email": user["email"], "name": user["name"]}
    jwt_token = google_service.create_jwt(payload)
    redirect_url = f"{FRONTEND_URL}/callback?token={jwt_token}"
    return RedirectResponse(url=redirect_url)