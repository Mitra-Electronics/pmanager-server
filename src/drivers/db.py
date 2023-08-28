# from os import getenv
from pathlib import Path
from sqlmodel import create_engine, Session

# CONNSTR = f'postgresql://{getenv("NEON_USERNAME")}:{getenv("NEON_PASSWD")}
# @{getenv("NEON_CLUSTER")}/{getenv("NEON_DB_NAME")}'
BASE_DIR = Path(__file__).parent.parent
CONNSTR = f"sqlite:///{BASE_DIR/ 'db.db'}"

engine = create_engine(CONNSTR, echo=True)


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
