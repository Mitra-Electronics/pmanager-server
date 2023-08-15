from sqlmodel import select, Session
from models import People


def db_get_person(session: Session, id_: int):
    return session.exec(select(People).where(People.id == id_)).first()
