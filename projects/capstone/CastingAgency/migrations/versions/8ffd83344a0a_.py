"""empty message

Revision ID: 8ffd83344a0a
Revises: 7bc90a31f4c8
Create Date: 2021-01-16 03:12:21.896584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ffd83344a0a'
down_revision = '7bc90a31f4c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('actor', sa.Column('name', sa.String(), nullable=False))
    op.drop_column('actor', 'names')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('actor', sa.Column('names', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('actor', 'name')
    # ### end Alembic commands ###
