"""add tkbfile

Revision ID: 1536ab89a18f
Revises: 5d29e689df70
Create Date: 2026-08-05 07:38:05.287362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1536ab89a18f'
down_revision = '5d29e689df70'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tkb_file',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('content', sa.LargeBinary(), nullable=False),
        sa.Column('week_start', sa.Date(), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), nullable=True),
        sa.Column('created_by_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('tkb_file')
