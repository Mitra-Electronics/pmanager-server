from sqlmodel import select, Session
from ..models import People
from .schemas import PeopleSchema


def db_get_person(session: Session, id_: int):
    return session.exec(select(People).where(People.id == id_)).first()


def db_add_person(session: Session, c: PeopleSchema, id: int | None):
    cdict = c.dict()
    cdict["user_id"] = id
    session.add(People(**cdict))
    session.commit()
