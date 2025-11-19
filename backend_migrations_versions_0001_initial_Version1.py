"""initial

Revision ID: 0001
Revises: 
Create Date: 2025-11-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=64), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=256), nullable=False),
        sa.Column('is_admin', sa.Boolean(), nullable=True)
    )
    op.create_table('cameras',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=128)),
        sa.Column('location', sa.String(length=256)),
        sa.Column('rtsp_url', sa.String(length=512))
    )
    op.create_table('jobs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('camera_id', sa.Integer(), nullable=True),
        sa.Column('source', sa.String(length=512)),
        sa.Column('status', sa.String(length=32), server_default='pending'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )
    op.create_table('alerts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('camera_id', sa.Integer(), nullable=True),
        sa.Column('job_id', sa.Integer(), nullable=True),
        sa.Column('severity', sa.String(length=32), server_default='low'),
        sa.Column('type', sa.String(length=64)),
        sa.Column('payload', sa.JSON()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )
    op.create_table('model_versions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('version', sa.String(length=64)),
        sa.Column('path', sa.String(length=512)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )


def downgrade():
    op.drop_table('model_versions')
    op.drop_table('alerts')
    op.drop_table('jobs')
    op.drop_table('cameras')
    op.drop_table('users')