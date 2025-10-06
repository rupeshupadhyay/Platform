import os, jwt
from typing import Dict


class CryptoService:
    """
    Service class for handling JWT-based authentication.
    Attributes:
        jwt_secret (str): Secret key used for encoding and decoding JWT tokens.
    Methods:
        create_jwt(payload: Dict) -> str:
            Generates a JWT token from the provided payload dictionary.
        decode_jwt(token: str) -> Dict:
            Decodes the provided JWT token and returns the payload as a dictionary.
    """
    def create_jwt(payload: Dict) -> str:
        print(os.getenv("JWT_SECRET"), "AuthService-----------------")
        return jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm="HS256")

    def decode_jwt(token: str) -> Dict:
        return jwt.decode(token,  os.getenv("JWT_SECRET"), algorithms=["HS256"])