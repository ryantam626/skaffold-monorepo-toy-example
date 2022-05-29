from sqlalchemy import Column, Integer, String

from fastapi_api.db.base_class import Base


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

    __tablename__ = "todo_items"
