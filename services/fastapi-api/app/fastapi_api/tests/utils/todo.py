from sqlalchemy.orm import Session

from fastapi_api import crud, models
from fastapi_api.schemas.todo import TodoItemCreate
from fastapi_api.tests.utils.utils import random_lower_string


def create_random_todo_item(db: Session) -> models.TodoItem:
    title = random_lower_string()
    description = random_lower_string()
    item_in = TodoItemCreate(title=title, description=description)
    return crud.todo_item.create(db=db, obj_in=item_in)
