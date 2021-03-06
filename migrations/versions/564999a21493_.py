"""empty message

Revision ID: 564999a21493
Revises: 01116a164e54
Create Date: 2020-05-11 18:26:30.649595

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '564999a21493'
down_revision = '01116a164e54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('icon', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('icon_ibfk_1', 'icon', type_='foreignkey')
    op.create_foreign_key(None, 'icon', 'user', ['user_id'], ['id'])
    op.drop_column('icon', 'profile_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('icon', sa.Column('profile_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'icon', type_='foreignkey')
    op.create_foreign_key('icon_ibfk_1', 'icon', 'user', ['profile_id'], ['id'])
    op.drop_column('icon', 'user_id')
    # ### end Alembic commands ###
