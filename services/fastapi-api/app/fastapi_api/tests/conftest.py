from typing import Generator

import pytest

from fastapi_api.db.session import SessionLocal


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()
