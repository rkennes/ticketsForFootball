from datetime import datetime
from pydantic import BaseModel

class sectorIn(BaseModel): 
    name: str 
    created_at: datetime | None = None    
