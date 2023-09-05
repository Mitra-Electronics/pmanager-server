from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from .crud import create_user, user_auth
from ..drivers.db import get_session
from .jwtd import create_access_token
from ..models import Login
from .schemas import UserInsert

router = APIRouter(tags=["Auth"])


@router.post("/login")
def login(login: Login, session: Session = Depends(get_session)):
    user_auth(session, login.email, login.password)
    return {"success": True, "result": create_access_token(login.email)}


@router.post("/token")
def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session)
):
    user_auth(session, form_data.username, form_data.password)

    return {
        "access_token": create_access_token(form_data.username),
        "token_type": "bearer"
    }


@router.post("/register")
def register(user: UserInsert, session: Session = Depends(get_session)):
    create_user(session, user)
    return {"success": True, "result": create_access_token(user.email)}
