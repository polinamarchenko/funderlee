"""Add Investor, Startup Class

Revision ID: e357a780bfa4
Revises: 
Create Date: 2017-05-27 22:41:33.685369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e357a780bfa4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('investors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('url', sa.Text(), nullable=True),
    sa.Column('country', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('startups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('url', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('startups_investors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('startup_id', sa.Integer(), nullable=True),
    sa.Column('investor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['investor_id'], ['investors.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['startup_id'], ['startups.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('startups_investors')
    op.drop_table('startups')
    op.drop_table('investors')
    # ### end Alembic commands ###