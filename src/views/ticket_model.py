from datetime import datetime
from pydantic import BaseModel

from typing import List

class TicketModelSectorOut(BaseModel):
    sector_id: int
    price: float
    ticket_load: int


class ticketModelOut(BaseModel):
    ticket_model_id: int
    cnpj: str
    name: str
    created_at: datetime
    sectors: List[TicketModelSectorOut]