"""Initial Migration

Revision ID: 8e806efdbf4a
Revises: 
Create Date: 2025-02-24 19:55:48.254282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e806efdbf4a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sector', sa.Integer(), nullable=False, server_default='0'))
        batch_op.add_column(sa.Column('action', sa.String(length=10), nullable=False, server_default='0'))

    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('action')
        batch_op.drop_column('sector')

    # ### end Alembic commands ###
