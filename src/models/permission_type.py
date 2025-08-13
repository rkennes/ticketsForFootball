import sqlalchemy as sa
from src.database import metadata

permission_type = sa.Table(
    "permission_type",
    metadata,
    sa.Column('cnpj', sa.String, nullable=False),
    sa.Column('permission_type', sa.Integer, nullable=False),
    sa.Column('description', sa.String, nullable=False),
    sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    sa.PrimaryKeyConstraint('cnpj', 'permission_type')
)
