"""empty message

Revision ID: d1c86ba10b15
Revises: 211bd851fe6a
Create Date: 2025-03-24 21:20:50.590629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1c86ba10b15'
down_revision = '211bd851fe6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('postagem', schema=None) as batch_op:
        batch_op.alter_column('conteudo',
               existing_type=sa.VARCHAR(),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('postagem', schema=None) as batch_op:
        batch_op.alter_column('conteudo',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(),
               existing_nullable=True)

    # ### end Alembic commands ###
