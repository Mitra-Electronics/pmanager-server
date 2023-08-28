from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from .crud import get_user, create_user
from ..drivers.db import get_session
from .pwd import verify_password
from .jwtd import create_access_token
from ..models import Login
from .schemas import UserInsert

router = APIRouter(tags=["Auth"])


@router.post("/login")
def login(login: Login, session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = get_user(session, login.email)
    if user is None:
        raise credentials_exception
    if not verify_password(login.password, user.hashed_password):
        raise credentials_exception
    return {"success": True, "result": create_access_token(login.email)}


@router.post("/register")
def register(user: UserInsert, session: Session = Depends(get_session)):
    create_user(session, user)
    return {"success": True, "result": create_access_token(user.email)}
