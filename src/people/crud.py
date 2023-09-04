from sqlmodel import select, Session
from ..models import People
from .schemas import PeopleSchema


def db_get_person(session: Session, id_: int, user_id: int):
    return session.exec(select(People)
                        .where(People.id == id_)
                        .where(People.user_id == user_id)).first()


def db_add_person(session: Session, c: PeopleSchema, id: int | None):
    cdict = c.dict()
    cdict["user_id"] = id
    cx = People(**cdict)
    session.add(cx)
    session.commit()
    return cx
