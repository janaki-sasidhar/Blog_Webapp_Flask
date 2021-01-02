"""empty message

Revision ID: d5f9b930781a
Revises: 9118d598d0ab
Create Date: 2021-01-02 11:36:32.186384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5f9b930781a'
down_revision = '9118d598d0ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dailyrecord',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('morningwalk', sa.Boolean(), nullable=False),
    sa.Column('waterdrank', sa.Integer(), nullable=False),
    sa.Column('breakfast', sa.Boolean(), nullable=False),
    sa.Column('breakfast_calories', sa.Integer(), nullable=False),
    sa.Column('lunch', sa.Boolean(), nullable=False),
    sa.Column('lunch_calories', sa.Integer(), nullable=False),
    sa.Column('dinner', sa.Boolean(), nullable=False),
    sa.Column('dinner_calories', sa.Integer(), nullable=False),
    sa.Column('total_calories', sa.Integer(), nullable=False),
    sa.Column('nightwalk', sa.Boolean(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('posted_or_not', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('paste', 'content',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('user', 'approved',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'approved',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('paste', 'content',
               existing_type=sa.TEXT(),
               nullable=True)
    op.drop_table('dailyrecord')
    # ### end Alembic commands ###