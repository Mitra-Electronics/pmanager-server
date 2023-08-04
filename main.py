from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import People
from sqlmodel import Session, select, delete, SQLModel
from drivers.db import engine

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


@app.post("/delete")
def delete_person(id: int):
    statement = delete(People).where(People.id == id)
    session.exec(statement)
    session.commit()
    return {"success": True}
