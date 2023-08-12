from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, delete, SQLModel
from schemas import People
from drivers.db import engine
from drivers.cloudinaryd import upload_img, delete_img

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
session = Session(engine)


@app.on_event("startup")
def start():
    SQLModel.metadata.create_all(engine)


@app.on_event("shutdown")
def shut():
    session.close()


@app.post("/add")
def add_person(c: People):
    session.add(c)
    session.commit()
    return {"success": True, "result": c.id}


@app.get("/get")
def get_all():
    statement = select(People)
    results = session.exec(statement)
    res = []
    for person in results:
        res.append(person.dict())
    return {"success": True, "result": res}


@app.get("/get/id")
def get_person(id: int):
    statement = select(People).where(People.id == id)
    results = session.exec(statement)
    res = None
    for person in results:
        res = person.dict()
    return {"success": True, "result": res}


@app.post("/edit")
def edit_person(id: int, update: People):
    statement = select(People).where(People.id == id)
    results = session.exec(statement)
    person: People = results.one()

    person.first_name = update.first_name
    person.last_name = update.last_name
    person.email = update.email
    person.birthday = update.birthday
    person.phone = update.phone
    person.github = update.github
    person.img = update.img
    person.instagram = update.instagram
    person.twitter = update.twitter
    person.country = update.country
    person.label = update.label

    session.add(person)
    session.commit()
    return {"success": True}


@app.post("/delete")
def delete_person(id: int, background_tasks: BackgroundTasks):
    statement = select(People).where(People.id == id)
    results = session.exec(statement)
    person: People = results.one()
    img = person.img
    statement = delete(People).where(People.id == id)
    session.exec(statement)
    session.commit()
    background_tasks.add_task(delete_img, img)
    return {"success": True}


@app.post("/upload")
def upload_file(file: UploadFile):
    url = upload_img(file.file)
    return {"success": True, "url": url}
