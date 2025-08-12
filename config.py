import os
from dotenv import load_dotenv

load_dotenv()  

SECRET = os.getenv("JWT_SECRET", "ticketsforfootball")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_ISSUER = "ticketsforfootball.com.br"
JWT_AUDIENCE = "ticketsforfootball"

DATABASE_URL = os.getenv("DATABASE_URL")
SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")

ENVIRONMENT = os.getenv("ENVIRONMENT", "local") 
