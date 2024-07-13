"""change type tring to text in the recipes n how_to_cook table model

Revision ID: a7268344a254
Revises: 9e859338719a
Create Date: 2024-07-13 06:51:55.238296

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a7268344a254'
down_revision = '9e859338719a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('how_to_cooks', schema=None) as batch_op:
        batch_op.alter_column('instructions',
                              existing_type=postgresql.ARRAY(sa.VARCHAR()),
                              type_=sa.ARRAY(sa.Text()),
                              existing_nullable=True,
                              postgresql_using='instructions::text[]')

    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.alter_column('instructions',
                              existing_type=postgresql.ARRAY(sa.VARCHAR()),
                              type_=sa.ARRAY(sa.Text()),
                              existing_nullable=True,
                              postgresql_using='instructions::text[]')

    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.alter_column('instructions',
                              existing_type=sa.ARRAY(sa.Text()),
                              type_=postgresql.ARRAY(sa.VARCHAR()),
                              existing_nullable=True,
                              postgresql_using='instructions::varchar[]')

    with op.batch_alter_table('how_to_cooks', schema=None) as batch_op:
        batch_op.alter_column('instructions',
                              existing_type=sa.ARRAY(sa.Text()),
                              type_=postgresql.ARRAY(sa.VARCHAR()),
                              existing_nullable=True,
                              postgresql_using='instructions::varchar[]')

    # ### end Alembic commands ###