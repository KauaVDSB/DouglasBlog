"""empty message

Revision ID: fde1bd69f58a
Revises: b0e6bc792f0f
Create Date: 2025-03-26 21:39:06.003104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fde1bd69f58a'
down_revision = 'b0e6bc792f0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('material', schema=None) as batch_op:
        batch_op.add_column(sa.Column('destino', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('titulo', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('material', schema=None) as batch_op:
        batch_op.drop_column('titulo')
        batch_op.drop_column('destino')

    # ### end Alembic commands ###
