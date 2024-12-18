"""empty message

Revision ID: 29b173b86030
Revises: 
Create Date: 2024-08-25 00:33:29.740035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29b173b86030'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('web_user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('identity', sa.String(length=50), nullable=True),
    sa.Column('username', sa.String(length=40), nullable=True),
    sa.Column('password', sa.String(length=40), nullable=True),
    sa.Column('access_token', sa.String(length=400), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('access_token'),
    sa.UniqueConstraint('username')
    )
    op.create_table('web_res',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('res_name', sa.String(length=50), nullable=True),
    sa.Column('res_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['res_id'], ['web_user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('res_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('web_res')
    op.drop_table('web_user')
    # ### end Alembic commands ###
