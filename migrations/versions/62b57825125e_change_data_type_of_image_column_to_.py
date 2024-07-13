"""Change data type of image column to ARRAY(db.Text)

Revision ID: 62b57825125e
Revises: f51360ea0410
Create Date: 2024-07-13 11:40:22.302136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62b57825125e'
down_revision = 'f51360ea0410'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('how_to_cooks', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.ARRAY(sa.Text()),
               existing_nullable=True,
               postgresql_using='instructions::text[]')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('how_to_cooks', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.ARRAY(sa.Text()),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True,
               postgresql_using='instructions::varchar[]')

    # ### end Alembic commands ###
