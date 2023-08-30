import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from src.drivers.db import get_session
from src.main import app


@pytest.fixture(name="session")
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


def test_register_unprocessable_user(client: TestClient):
    response = client.post(
        "/register/",
        json={
            "email": "user@example.com",
            "password": "123"
        }
    )
    assert response.status_code == 422


def test_register_empty_user(client: TestClient):
    response = client.post(
        "/register/",
        json={
            "email": "user@example.com",
            "password": "123",
            "first_name": "",
            "last_name": "",
            "country": "India"
        }
    )
    assert response.status_code == 422


def test_register_user(client: TestClient):
    response = client.post(
        "/register/",
        json={
            "email": "user@example.com",
            "password": "123",
            "first_name": "Example",
            "last_name": "Surname",
            "country": "India"
        }
    )
    assert response.status_code == 200
    content = response.json()
    assert content["success"] is True


def test_login_user_wrong_email(client: TestClient):
    response = client.post(
        "/login/",
        json={
            "email": "usernone@example.com",
            "password": "123"
        }
    )
    assert response.status_code == 401


def test_login_user_wrong_password(client: TestClient):
    response = client.post(
        "/login/",
        json={
            "email": "user@example.com",
            "password": "ioj"
        }
    )
    assert response.status_code == 401


def test_login_user_right_password(client: TestClient):
    response = client.post(
        "/login/",
        json={
            "email": "user@example.com",
            "password": "123"
        }
    )
    assert response.status_code == 200
