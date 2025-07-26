import sqlalchemy as sa
from src.database import metadata

event_service = sa.Table(
    "event_service",
    metadata,
    sa.Column("cnpj", sa.String),
    sa.Column("event_service_id", sa.Integer),
    sa.Column("ticket_model_id", sa.Integer),
    sa.Column("name", sa.String),
    sa.Column("event_date", sa.Date),
    sa.Column("event_address", sa.String),
    sa.Column("event_description", sa.String),
    sa.Column("user", sa.String),
    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    sa.PrimaryKeyConstraint('cnpj', 'event_service_id')
)
