"""fixed the response display settings in the instructions column in the how_to_cook model table

Revision ID: 9e859338719a
Revises: af11b382b2c6
Create Date: 2024-07-13 06:45:57.454667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e859338719a'
down_revision = 'af11b382b2c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('how_to_cooks', schema=None) as batch_op:
        batch_op.alter_column('instructions',
                              type_=sa.ARRAY(sa.String),
                              postgresql_using='instructions::character varying[]',
                              existing_type=sa.Text)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('how_to_cooks', schema=None) as batch_op:
        batch_op.alter_column('instructions',
                              type_=sa.Text,
                              postgresql_using='instructions::text',
                              existing_type=sa.ARRAY(sa.String))


    # ### end Alembic commands ###
