"""empty message

Revision ID: 51f732aa5466
Revises: c55351613d16
Create Date: 2020-12-25 21:47:27.090205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51f732aa5466'
down_revision = 'c55351613d16'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ingredient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('calories', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('measure',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('measure_qty',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=True),
    sa.Column('description', sa.String(length=840), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recipe_timestamp'), 'recipe', ['timestamp'], unique=False)
    op.create_table('recipe_ingredient',
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('measure_id', sa.Integer(), nullable=True),
    sa.Column('measure_qty_id', sa.Integer(), nullable=True),
    sa.Column('ingredient_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ingredient_id'], ['ingredient.id'], ),
    sa.ForeignKeyConstraint(['measure_id'], ['measure.id'], ),
    sa.ForeignKeyConstraint(['measure_qty_id'], ['measure_qty.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipe_ingredient')
    op.drop_index(op.f('ix_recipe_timestamp'), table_name='recipe')
    op.drop_table('recipe')
    op.drop_table('measure_qty')
    op.drop_table('measure')
    op.drop_table('ingredient')
    # ### end Alembic commands ###
