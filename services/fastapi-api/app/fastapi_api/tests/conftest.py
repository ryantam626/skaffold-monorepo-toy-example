import os
from typing import Generator

import pytest
from pydantic import PostgresDsn
from sqlalchemy import create_engine, text
from starlette.testclient import TestClient

from fastapi_api.main import app

TEST_DB_CREATED = False


def maybe_create_test_database() -> None:
    global TEST_DB_CREATED
    if not TEST_DB_CREATED:
        test_database = "test_{database}".format(
            database=os.environ["POSTGRES_DB"],
        )

        engine = create_engine(
            PostgresDsn.build(
                scheme="postgresql",
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD"),
                host=os.environ.get("POSTGRES_SERVER"),
                path=f"/{os.environ.get('POSTGRES_DB')}",
            )
        )

        connection = engine.connect()

        connection.execute("COMMIT")
        connection.execute(
            f"""
                DROP DATABASE IF EXISTS {test_database}
            """
        )

        # Kick people out temporarily to run CREATE DATABASE WITH TEMPLATE later
        connection.execute("COMMIT")
        connection.execute(
            text(
                """
                    SELECT
                        pg_terminate_backend(pg_stat_activity.pid)
                    FROM
                        pg_stat_activity
                    WHERE
                        pg_stat_activity.datname = :db
                    AND pid <> pg_backend_pid();
                """
            ),
            db=os.environ["POSTGRES_DB"],
        )

        connection.execute("COMMIT")
        connection.execute(
            """
                CREATE DATABASE {test_database}
                WITH TEMPLATE {database}
                OWNER {user};
            """.format(
                test_database=test_database,
                database=os.environ["POSTGRES_DB"],
                user=os.environ["POSTGRES_USER"],
            )
        )
        os.environ["POSTGRES_DB"] = test_database
        TEST_DB_CREATED = True


@pytest.fixture(scope="session")
def db() -> Generator:
    maybe_create_test_database()
    from fastapi_api.db.session import SessionLocal

    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
