from fastapi_api.crud.base import CRUDBase
from fastapi_api.models.todo import TodoItem
from fastapi_api.schemas.todo import TodoItemCreate, TodoItemUpdate


class CRUDTodoItem(CRUDBase[TodoItem, TodoItemCreate, TodoItemUpdate]):
    pass


todo_item = CRUDTodoItem(TodoItem)
