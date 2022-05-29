from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi_api import crud, schemas
from fastapi_api.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.TodoItem])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Retrieve items."""
    return crud.todo_item.get_multi(db=db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.TodoItem)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.TodoItemCreate,
) -> Any:
    """Create new item."""
    return crud.todo_item.create(db=db, obj_in=item_in)


@router.put("/{id}", response_model=schemas.TodoItem)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: schemas.TodoItemUpdate,
) -> Any:
    """Update an item."""
    todo_item = crud.todo_item.get(db=db, id=id)
    if not todo_item:
        raise HTTPException(status_code=404, detail="Item not found")
    todo_item = crud.todo_item.update(db=db, db_obj=todo_item, obj_in=item_in)
    return todo_item


@router.get("/{id}", response_model=schemas.TodoItem)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """Get item by ID."""
    todo_item = crud.todo_item.get(db=db, id=id)
    if not todo_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return todo_item


@router.delete("/{id}", response_model=schemas.TodoItem)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """Delete an item."""
    todo_item = crud.todo_item.get(db=db, id=id)
    if not todo_item:
        raise HTTPException(status_code=404, detail="Item not found")
    todo_item = crud.todo_item.remove(db=db, id=id)
    return todo_item
