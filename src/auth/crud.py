from sqlmodel import Session, select
from ..models import User


def get_user(db: Session, email: str):
    return db.exec(select(User).where(User.email == email)).first()
