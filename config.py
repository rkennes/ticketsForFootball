import os

SECRET = os.getenv("JWT_SECRET", "ticketsforfootball")  
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_ISSUER = "ticketsforfootball.com.br"
JWT_AUDIENCE = "ticketsforfootball"