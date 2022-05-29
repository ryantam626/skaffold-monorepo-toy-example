from typing import Optional

from pydantic import BaseModel


# Shared properties
class TodoItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class TodoItemCreate(TodoItemBase):
    title: str


# Properties to receive on item update
class TodoItemUpdate(TodoItemBase):
    pass


# Properties shared by models stored in DB
class TodoItemInDBBase(TodoItemBase):
    id: int
    title: str

    class Config:
        orm_mode = True


# Properties to return to client
class TodoItem(TodoItemInDBBase):
    pass


# Properties properties stored in DB
class TodoItemInDB(TodoItemInDBBase):
    pass
