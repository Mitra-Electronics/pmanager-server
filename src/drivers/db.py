from pathlib import Path
from sqlmodel import create_engine, Session
from .envd import get_env


CONNSTR = get_env(
    "CONNSTR",
    f"sqlite:///{Path(__file__).parent.parent/ 'db.db'}"
)

engine = create_engine(CONNSTR, echo=True)


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
