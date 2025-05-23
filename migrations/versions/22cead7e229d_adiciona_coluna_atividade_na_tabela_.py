"""Adiciona coluna Atividade na tabela Material

Revision ID: 22cead7e229d
Revises: ce4c175d4b49
Create Date: 2025-05-12 16:17:33.584760

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "22cead7e229d"
down_revision = "ce4c175d4b49"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("material", schema=None) as batch_op:
        batch_op.add_column(sa.Column("atividade", sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("material", schema=None) as batch_op:
        batch_op.drop_column("atividade")

    # ### end Alembic commands ###
