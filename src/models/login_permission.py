import sqlalchemy as sa
from src.database import metadata

login_permission = sa.Table(
    "login_permission",
    metadata,
    sa.Column('cnpj', sa.String, nullable=False),
    sa.Column('email', sa.String, nullable=False),
    sa.Column('password', sa.String, nullable=False),
    sa.Column('name', sa.String, nullable=False),
    sa.Column('permission_type', sa.Integer, nullable=False),
    sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    sa.PrimaryKeyConstraint('cnpj', 'email')
)
