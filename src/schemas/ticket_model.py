from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class TicketModelSectorIn(BaseModel):
    sector_id: int
    price: float
    ticket_load: int

class TicketModelIn(BaseModel):
    name: str
    created_at: datetime | None = None
    sectors: List[TicketModelSectorIn]

class TicketModelSectorUpdate(BaseModel):
    sector_id: int
    price: Optional[float] = None
    ticket_load: Optional[int] = None
    
class TicketModelUpdate(BaseModel):
    name: Optional[str] = None                 
    sectors: List[TicketModelSectorUpdate] = []  