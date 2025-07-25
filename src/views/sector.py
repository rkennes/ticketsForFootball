from datetime import datetime
from pydantic import BaseModel

class sectorOut(BaseModel): 
    cnpj: str
    sector_id: int
    name: str 
    created_at: datetime | None = None    
