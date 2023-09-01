from fastapi import APIRouter, Depends, UploadFile, BackgroundTasks
from sqlmodel import Session, select, delete
from ..drivers.cloudinaryd import upload_img, delete_img
from ..drivers.db import get_session
from .crud import db_get_person, db_add_person

from ..models import People

router = APIRouter(tags=["People"])


@router.post("/add")
def add_person(c: People, session: Session = Depends(get_session)):
    db_add_person(session, c)
    return {"success": True, "result": c.id}


@router.get("/get")
def get_all(session: Session = Depends(get_session)):
    statement = select(People)
    results = session.exec(statement).fetchall()
    res = [x.dict() for x in results]
    return {"success": True, "result": res}


@router.get("/get/id")
def get_person(id: int, session: Session = Depends(get_session)):
    results = db_get_person(session, id)
    if results:
        return {"success": True, "result": results}
    return {"success": False, "reason": "Does not exist"}


@router.post("/edit")
def edit_person(
    id: int,
    update: People,
    session: Session = Depends(get_session)
):
    person: People | None = db_get_person(session, id)

    if person is None:
        return {"success": False, "reason": "Does not exist"}

    person_data = update.dict(exclude_unset=True)
    for key, value in person_data.items():
        setattr(person, key, value)

    session.add(person)
    session.commit()
    return {"success": True}


@router.post("/delete")
def delete_person(
        id: int,
        background_tasks: BackgroundTasks,
        session: Session = Depends(get_session)
):
    person: People | None = db_get_person(session, id)
    if person is None:
        return {"success": False, "reason": "Does not exist"}
    img = person.img
    statement = delete(People).where(People.id == id)
    session.exec(statement)  # type: ignore
    session.commit()
    if img:
        background_tasks.add_task(delete_img, img)
    return {"success": True}


@router.post("/upload")
def upload_file(file: UploadFile):
    url = upload_img(file.file)
    return {"success": True, "url": url}
