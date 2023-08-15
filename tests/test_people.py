import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from drivers.db import get_session
from main import app
import os
from pathlib import Path
BASE_DIR = Path(__file__).parent.parent


@pytest.fixture(name="session")  # type: ignore
def session_fixture():
    engine = create_engine(
        "sqlite:///test.db", connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_add_person(client: TestClient):
    response = client.post(
        "/add/", json={"first_name": "Deadpond", "last_name": "Wilson"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
    assert type(data["result"]) is int
    assert data["result"] == 1


def test_get_all(client: TestClient):
    resp = client.get("/get")
    data = resp.json()

    assert resp.status_code == 200
    assert data["success"] is True
    assert data["result"] is not False
    assert len(data["result"]) == 1
    assert type(data["result"]) is list
    assert type(data["result"][0]) is dict
    assert data["result"][0]["first_name"] == "Deadpond"
    assert data["result"][0]["last_name"] == "Wilson"
    assert data["result"][0]["id"] == 1
    items = data["result"][0].items()
    assert len(items) == 12
    for k, v in items:
        if k != "first_name" and k != "last_name" and k != "id":
            assert v is None


def test_get_one_found(client: TestClient):
    resp = client.get("/get/id", params={"id": 1})
    data = resp.json()
    assert resp.status_code == 200
    assert data["success"] is True
    assert data["result"] is not False
    assert type(data["result"]) is dict
    assert data["result"]["first_name"] == "Deadpond"
    assert data["result"]["last_name"] == "Wilson"
    assert data["result"]["id"] == 1
    items = data["result"].items()
    assert len(items) == 12
    for k, v in items:
        if k != "first_name" and k != "last_name" and k != "id":
            assert v is None


def test_get_one_not_found(client: TestClient):
    resp = client.get("/get/id", params={"id": 2})
    data = resp.json()
    assert resp.status_code == 200
    assert data["success"] is False
    assert data["reason"] == "Does not exist"


def test_database_delete():
    assert os.path.exists(BASE_DIR / "test.db")
    os.remove("test.db")
    assert not os.path.exists(BASE_DIR / "test.db")
