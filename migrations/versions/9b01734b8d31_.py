"""empty message

Revision ID: 9b01734b8d31
Revises: 1b5f500cccf5
Create Date: 2021-12-14 13:07:05.604213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b01734b8d31'
down_revision = '1b5f500cccf5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bankdetails',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('account_name', sa.String(length=150), nullable=False),
    sa.Column('account_number', sa.String(length=20), nullable=False),
    sa.Column('bank_name', sa.String(length=100), nullable=False),
    sa.Column('craftsp_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['craftsp_id'], ['craftsperson.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bankdetails')
    # ### end Alembic commands ###
