from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from amigo.auth.auth_service import AuthService

auth_service = AuthService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[str]:
    """
    Dependency function to extract the user email from the access token.

    Args:
        token (str): The access token provided by the client.

    Raises:
        HTTPException: If the access token is invalid or expired.

    Returns:
        Optional[str]: The user email if the token is valid, otherwise None.
    """
    try:
        payload = auth_service.verify_access_token(token)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
