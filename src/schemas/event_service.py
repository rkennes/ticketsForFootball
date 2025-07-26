from datetime import date, datetime
from pydantic import BaseModel

class EventServiceIn(BaseModel):
    cnpj: str
    ticket_model_id: int
    name: str
    event_date: date
    event_address: str
    event_description: str

class EventServiceUpdate(BaseModel):
    ticket_model_id: int
    name: str
    event_date: date
    event_address: str
    event_description: str

