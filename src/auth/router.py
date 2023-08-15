from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from auth.crud import get_user
from drivers.db import get_session
from models import Login

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
    return user


@router.post("/register")
def register():
    pass
