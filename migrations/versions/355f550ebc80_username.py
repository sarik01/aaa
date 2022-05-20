"""'username'

Revision ID: 355f550ebc80
Revises: 37635305b4a4
Create Date: 2022-05-06 17:28:18.424641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '355f550ebc80'
down_revision = '37635305b4a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(length=20), nullable=False))
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###