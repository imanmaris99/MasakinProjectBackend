"""Add food_name n food_image column in recipes table n also downgrade food table

Revision ID: da2325b0c4ac
Revises: bbc2f8992734
Create Date: 2024-07-11 12:53:58.230961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da2325b0c4ac'
down_revision = 'bbc2f8992734'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rating_recipe', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recipe_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'recipes', ['recipe_id'], ['id'])
        batch_op.drop_column('food_id')

    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('food_name', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('food_image', sa.String(length=255), nullable=True))
        batch_op.drop_column('food_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('food_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('food_image')
        batch_op.drop_column('food_name')

    with op.batch_alter_table('rating_recipe', schema=None) as batch_op:
        batch_op.add_column(sa.Column('food_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('recipe_id')

    # ### end Alembic commands ###
