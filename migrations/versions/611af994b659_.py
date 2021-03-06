"""empty message

Revision ID: 611af994b659
Revises: 
Create Date: 2021-03-02 15:44:52.307940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '611af994b659'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=20), nullable=False),
    sa.Column('slug', sa.String(length=10), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('link')
    # ### end Alembic commands ###
