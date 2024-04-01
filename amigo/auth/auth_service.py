from datetime import datetime, timedelta
from os import getenv
from typing import Optional

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = 120


class AuthService:
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.
        """
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Hash a plain password using the configured password context.
        """
        return pwd_context.hash(password)

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create an access token using the provided data and expiration time.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_access_token(self, token: str) -> dict:
        """
        Verify and decode an access token.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.JWTError:
            raise Exception("Invalid access token")
