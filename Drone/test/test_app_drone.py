import json
import os
import sys
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from routes.drone import router_drone
from schemas.database import Base, get_db

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def start_application():
    app = FastAPI()
    app.include_router(router_drone)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(
        app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


def test_create_drone_pass(client):
    data = {
        "id": 1,
        "serial_number": "946589",
        "model": "Lightweight",
        "weight_limit": 50,
        "battery_capacity": 100,
        "state": "IDLE",
        "medications": []
    }
    response = client.post("/drone/create/", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["weight_limit"] <= 500
    assert response.json()["state"] == "IDLE"


def test_create_drone_failed_registred(client):
    data = {
        "id": 1,
        "serial_number": "946589",
        "model": "Lightweight",
        "weight_limit": 501,
        "battery_capacity": 100,
        "state": "IDLE",
        "medications": []
    }
    response = client.post("/drone/create/", json.dumps(data))
    assert response.status_code == 404
    print(response.json())


def test_create_drone_failed_weight(client):
    data = {
        "id": 2,
        "serial_number": "946589123",
        "model": "Lightweight",
        "weight_limit": 501,
        "battery_capacity": 100,
        "state": "IDLE",
        "medications": []
    }
    response = client.post("/drone/create/", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["weight_limit"] <= 500
