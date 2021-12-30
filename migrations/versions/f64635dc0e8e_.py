"""empty message

Revision ID: f64635dc0e8e
Revises: 
Create Date: 2021-12-04 19:13:35.376827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f64635dc0e8e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('craftsperson', sa.Column('service_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'craftsperson', 'service', ['service_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'craftsperson', type_='foreignkey')
    op.drop_column('craftsperson', 'service_id')
    # ### end Alembic commands ###