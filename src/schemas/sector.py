from datetime import datetime
from pydantic import BaseModel

class sectorIn(BaseModel): 
    cnpj: str
    name: str 
    created_at: datetime | None = None    
