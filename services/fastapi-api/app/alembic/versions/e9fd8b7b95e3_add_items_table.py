"""Add items table

Revision ID: e9fd8b7b95e3
Revises: 
Create Date: 2022-05-29 18:14:49.307350

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "e9fd8b7b95e3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "todo_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_todo_items_description"), "todo_items", ["description"], unique=False)
    op.create_index(op.f("ix_todo_items_id"), "todo_items", ["id"], unique=False)
    op.create_index(op.f("ix_todo_items_title"), "todo_items", ["title"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_todo_items_title"), table_name="todo_items")
    op.drop_index(op.f("ix_todo_items_id"), table_name="todo_items")
    op.drop_index(op.f("ix_todo_items_description"), table_name="todo_items")
    op.drop_table("todo_items")
