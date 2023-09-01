from sqlmodel import Session

from .crud import get_user
from .jwtd import decode_access_token
from fastapi import HTTPException, status


def get_current_user(token: str, session: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = decode_access_token(token)
    user = get_user(session, email)
    if user is None:
        raise credentials_exception
    return user
