import sqlalchemy as sa
from src.database import metadata

ticket_model = sa.Table(
    "ticket_model",
    metadata,
    sa.Column("cnpj", sa.String, primary_key=True),
    sa.Column("ticket_model_id", sa.Integer, primary_key=True),
    sa.Column("sector_id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String),
    sa.Column("price", sa.Float),
    sa.Column("ticket_load", sa.Integer),
    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
)
