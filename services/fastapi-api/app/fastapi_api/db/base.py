# Import all the models, so that Base has them before being
# imported by Alembic
from fastapi_api.db.base_class import Base  # noqa
from fastapi_api.models.todo import Item  # noqa
