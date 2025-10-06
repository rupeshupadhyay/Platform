
import httpx, os
from urllib.parse import urlencode
from typing import Dict
from app.services.crypto_service import CryptoService

class GithubAuthService(CryptoService):
    def __init__(self):
        self.client_id = os.getenv("GITHUB_CLIENT_ID")
        self.client_secret = os.getenv("GITHUB_CLIENT_SECRET")
        self.github_token_url = os.getenv("GITHUB_TOKEN_URL")
        self.github_user_url = os.getenv("GITHUB_USER_INFO_URL")

    def get_auth_url(self) -> str:
        params = {
            "client_id": self.client_id,
            "scope": "read:user user:email",
            "allow_signup": "true",
            "prompt": "login"
        }
        return f"https://github.com/login/oauth/authorize?{urlencode(params)}"

    async def exchange_code_for_token(self, code: str) -> str:
        async with httpx.AsyncClient() as client:
            token_res = await client.post(
                self.github_token_url,
                headers={"Accept": "application/json"},
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                },
            )
            token_json = token_res.json()
            return token_json.get("access_token")

    async def get_user(self, access_token: str) -> Dict:
        async with httpx.AsyncClient() as client:
            user_res = await client.get(
                self.github_user_url,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            return user_res.json()
    
    def create_jwt(self, payload: Dict) -> str:
        print(payload, "GithubAuth-----------------")
        print(os.getenv("JWT_SECRET"), "GithubAuth-----------------")
        return CryptoService.create_jwt(payload)
    
    def decode_jwt(self, token: str) -> Dict:
        return CryptoService.decode_jwt(token)