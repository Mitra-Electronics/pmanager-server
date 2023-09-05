import os
from pathlib import Path
BASE_DIR = Path(__file__).parent.parent


def pytest_unconfigure(config):
    assert os.path.exists(BASE_DIR / "test.db")
    os.remove("test.db")
    assert not os.path.exists(BASE_DIR / "test.db")
