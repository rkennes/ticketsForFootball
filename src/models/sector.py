import sqlalchemy as sa
from src.database import metadata

sector = sa.Table(
    "sector",
    metadata,
    sa.Column('cnpj', sa.String, nullable=False),
    sa.Column('sector_id', sa.Integer, nullable=False),
    sa.Column('name', sa.String),
    sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    sa.PrimaryKeyConstraint('cnpj','sector_id')
)
