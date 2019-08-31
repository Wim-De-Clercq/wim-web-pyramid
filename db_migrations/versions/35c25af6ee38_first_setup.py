"""first setup

Revision ID: 35c25af6ee38
Revises:
Create Date: 2019-07-24 23:00:54.399944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35c25af6ee38'
down_revision = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('admin', sa.Boolean, nullable=False, default=False,
                  server_default='false'),
        sa.Column('pw_hash', sa.String, nullable=False),
    )
    op.create_table(
        'items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'),
                  nullable=False),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False)
    )
    op.create_table(
        'files',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('extension', sa.String(length=5), nullable=False),
        sa.Column('item_id', sa.Integer, nullable=False)
    )
