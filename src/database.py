import sqlalchemy as sa
import databases
from src.config import settings

database = databases.Database(settings.database_url)
metadata = sa.MetaData()
engine = sa.create_engine(settings.database_url.replace('+asyncpg', ''), pool_pre_ping=True)
