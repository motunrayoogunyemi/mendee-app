"""empty message

Revision ID: 07a27bfd4cc1
Revises: a814771f1745
Create Date: 2021-12-13 16:54:11.873909

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '07a27bfd4cc1'
down_revision = 'a814771f1745'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mybookings', sa.Column('btrx_ref', sa.String(length=12), nullable=False))
    op.drop_column('mybookings', 'trx_ref')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mybookings', sa.Column('trx_ref', mysql.VARCHAR(length=12), nullable=False))
    op.drop_column('mybookings', 'btrx_ref')
    # ### end Alembic commands ###