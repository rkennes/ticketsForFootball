import sqlalchemy as sa
from src.database import metadata

ticket_model = sa.Table(
    "ticket_model",
    metadata,
    sa.Column("cnpj", sa.String),
    sa.Column("ticket_model_id", sa.Integer),
    sa.Column("name", sa.String),
    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    sa.PrimaryKeyConstraint('cnpj', 'ticket_model_id')
)

ticket_model_sector = sa.Table(
    "ticket_model_sector",
    metadata,
    sa.Column("cnpj", sa.String),
    sa.Column("ticket_model_id", sa.Integer),
    sa.Column("sector_id", sa.Integer),
    sa.Column("price", sa.Float),
    sa.Column("ticket_load", sa.Integer),
    sa.PrimaryKeyConstraint('cnpj', 'ticket_model_id', 'sector_id')
)
