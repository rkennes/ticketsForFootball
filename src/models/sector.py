import sqlalchemy as sa
from src.database import metadata

sector = sa.Table(
    "sector",
    metadata,
    sa.Column("cnpj", sa.String, primary_key=True),
    sa.Column("sector_id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String),
    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
)
