import httpx, os
from urllib.parse import urlencode
from typing import Dict
from app.services.crypto_service import CryptoService

class GoogleAuthService(CryptoService):
    def __init__(self):
        self.client_id =os.getenv("GOOGLE_CLIENT_ID")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.auth_url=os.getenv("GOOGLE_AUTH_URL")
        self.token_url =os.getenv("GOOGLE_TOKEN_URL")
        self.user_info_url = os.getenv("GOOGLE_USER_INFO_URL")
        self.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

    def get_auth_url(self) -> str:
        params = {
            "client_id": self.client_id ,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent"
        }
        return f"{self.auth_url}?{urlencode(params)}"

    async def exchange_code_for_token(self, code: str) -> str:
        async with httpx.AsyncClient() as client:
            data = {
                "code": code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
                "grant_type": "authorization_code",
            }
            token_res = await client.post(self.token_url, data=data)
            token_json = token_res.json()
            return token_json.get("access_token")

    async def get_user(self, access_token: str) -> Dict:
        async with httpx.AsyncClient() as client:
            user_res = await client.get(
                self.user_info_url,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            return user_res.json()
        
    def create_jwt(self, payload: Dict) -> str:
        return CryptoService.create_jwt(payload)
    
    def decode_jwt(self, token: str) -> Dict:
        return CryptoService.decode_jwt(token)