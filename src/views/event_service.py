from datetime import datetime,date
from pydantic import BaseModel


class EventServiceOut(BaseModel):
    cnpj: str
    ticket_model_id: int
    name: str
    event_date: date
    event_address: str
    event_description: str
    event_service_id: int
    created_at: datetime

