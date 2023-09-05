from fastapi import HTTPException, status
from sqlmodel import Session, select
from ..models import User
from .schemas import UserInsert
from .pwd import get_password_hash, verify_password


def get_user(db: Session, email: str):
    return db.exec(select(User).where(User.email == email)).first()


def create_user(db: Session, c: UserInsert):
    c_dict = c.dict()
    c_dict["hashed_password"] = get_password_hash(c.password)
    c_dict.pop("password")
    obj = User(**c_dict)
    db.add(obj)
    db.commit()


def user_auth(session: Session, email: str, password: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = get_user(session, email)
    if user is None:
        raise credentials_exception
    if not verify_password(password, user.hashed_password):
        raise credentials_exception
