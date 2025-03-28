"""empty message

Revision ID: 7e6ea11d14c7
Revises: dae292ebcb82
Create Date: 2025-03-27 21:29:17.642525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e6ea11d14c7'
down_revision = 'dae292ebcb82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('material', schema=None) as batch_op:
        batch_op.add_column(sa.Column('materiais', sa.Text(), nullable=True))
        batch_op.drop_column('material_mapa')
        batch_op.drop_column('material_aula')
        batch_op.drop_column('material_exercicios')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('material', schema=None) as batch_op:
        batch_op.add_column(sa.Column('material_exercicios', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('material_aula', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('material_mapa', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.drop_column('materiais')

    # ### end Alembic commands ###
