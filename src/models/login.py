import sqlalchemy as sa
from src.database import metadata

login = sa.Table(
    "login",
    metadata,
    sa.Column('cnpj', sa.String, nullable=False),
    sa.Column('email', sa.String, nullable=False),
    sa.Column('password', sa.String, nullable=False),
    sa.Column('corporate_name', sa.String, nullable=False),
    sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    sa.PrimaryKeyConstraint('cnpj'),
    sa.Index('ix_login_email_password', 'email', 'password')
)
