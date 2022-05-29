from sqlalchemy.orm import Session

from fastapi_api import crud
from fastapi_api.schemas.todo import TodoItemCreate, TodoItemUpdate
from fastapi_api.tests.utils.utils import random_lower_string


def test_create_todo_item(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    todo_item_in = TodoItemCreate(title=title, description=description)
    todo_item = crud.todo_item.create(db, obj_in=todo_item_in)

    assert todo_item.title == title
    assert todo_item.description == description


def test_get_todo_item(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    todo_item_in = TodoItemCreate(title=title, description=description)
    todo_item = crud.todo_item.create(db, obj_in=todo_item_in)
    stored_todo_item = crud.todo_item.get(db=db, id=todo_item.id)

    assert stored_todo_item
    assert todo_item.id == stored_todo_item.id
    assert todo_item.title == stored_todo_item.title
    assert todo_item.description == stored_todo_item.description


def test_update_todo_item(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    todo_item_in = TodoItemCreate(title=title, description=description)
    todo_item = crud.todo_item.create(db, obj_in=todo_item_in)
    description2 = random_lower_string()
    todo_item_update = TodoItemUpdate(description=description2)
    todo_item2 = crud.todo_item.update(db=db, db_obj=todo_item, obj_in=todo_item_update)

    assert todo_item.id == todo_item2.id
    assert todo_item.title == todo_item2.title
    assert todo_item2.description == description2


def test_delete_todo_item(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    todo_item_in = TodoItemCreate(title=title, description=description)
    todo_item = crud.todo_item.create(db, obj_in=todo_item_in)
    todo_item2 = crud.todo_item.remove(db=db, id=todo_item.id)
    todo_item3 = crud.todo_item.get(db=db, id=todo_item.id)

    assert todo_item3 is None
    assert todo_item2.id == todo_item.id
    assert todo_item2.title == title
    assert todo_item2.description == description
