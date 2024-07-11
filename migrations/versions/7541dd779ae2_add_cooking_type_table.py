"""add cooking_type table

Revision ID: 7541dd779ae2
Revises: a72566c74751
Create Date: 2024-07-10 18:56:37.580074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7541dd779ae2'
down_revision = 'a72566c74751'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cooking_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('info', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cooking_type')
    # ### end Alembic commands ###