from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .drivers.db import engine
from sqlmodel import SQLModel
from .models import People, User  # noqa
from .people.router import router as prouter
from .auth.router import router as arouter

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=prouter)
app.include_router(router=arouter)


@app.on_event("startup")
def start():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def status():
    return {"status": "ok"}
