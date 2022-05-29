from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from fastapi_api.core.config import settings
from fastapi_api.tests.utils.todo import create_random_todo_item


def test_create_item(client: TestClient, db: Session) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/todos/",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content


def test_read_item(client: TestClient, db: Session) -> None:
    todo_item = create_random_todo_item(db)
    response = client.get(
        f"{settings.API_V1_STR}/todos/{todo_item.id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == todo_item.title
    assert content["description"] == todo_item.description
    assert content["id"] == todo_item.id
