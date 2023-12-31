"""empty message

Revision ID: 063be5f7c18a
Revises: 
Create Date: 2023-07-23 22:16:26.358353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '063be5f7c18a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=5000), nullable=False),
    sa.Column('description', sa.String(length=5000), nullable=False),
    sa.Column('category', sa.String(length=5000), nullable=False),
    sa.Column('image', sa.String(length=5000), nullable=False),
    sa.Column('rating', sa.Float(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cart')
    op.drop_table('product')
    # ### end Alembic commands ###
