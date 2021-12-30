"""empty message

Revision ID: 5af6a8f5ab12
Revises: aef01d346982
Create Date: 2021-12-13 17:11:23.648135

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5af6a8f5ab12'
down_revision = 'aef01d346982'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('mybookings', 'btimedate_month',
               existing_type=mysql.VARCHAR(length=55),
               nullable=True)
    op.alter_column('mybookings', 'btimedate_date',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True)
    op.alter_column('mybookings', 'btimedate_time',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('mybookings', 'btimedate_time',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False)
    op.alter_column('mybookings', 'btimedate_date',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False)
    op.alter_column('mybookings', 'btimedate_month',
               existing_type=mysql.VARCHAR(length=55),
               nullable=False)
    # ### end Alembic commands ###