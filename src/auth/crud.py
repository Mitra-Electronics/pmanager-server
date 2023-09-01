from sqlmodel import Session, select
from ..models import User
from .schemas import UserInsert
from .pwd import get_password_hash


def get_user(db: Session, email: str):
    return db.exec(select(User).where(User.email == email)).first()


def create_user(db: Session, c: UserInsert):
    c_dict = c.dict()
    c_dict["hashed_password"] = get_password_hash(c.password)
    c_dict.pop("password")
    obj = User(**c_dict)
    db.add(obj)
    db.commit()
