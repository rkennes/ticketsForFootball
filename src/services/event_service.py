from fastapi import HTTPException, status
from sqlalchemy import select, func
from src.models.event_service import event_service
from src.models.ticket_model import ticket_model
from src.database import database
from src.schemas.event_service import EventServiceIn, EventServiceUpdate
from databases.interfaces import Record
from src.services.ticket_model import TicketModelService

class EventService:

    async def read_event_service(self, cnpj: str) -> list[Record]:
        query = event_service.select().where(event_service.c.cnpj == cnpj)
        return await database.fetch_all(query)

    async def create_event_service(self, data: EventServiceIn, cnpj: str) -> dict:
        
        validate_ticketModel = await TicketModelService._validate_model(cnpj, data.ticket_model_id)
        if not validate_ticketModel:
            return  
      
        query_max_id = select(func.max(event_service.c.event_service_id)).where(
            event_service.c.cnpj == cnpj
        )
        last_id = await database.fetch_val(query_max_id) or 0
        next_id = last_id + 1

        await database.execute(event_service.insert().values(
            cnpj=cnpj,
            event_service_id=next_id,
            ticket_model_id=data.ticket_model_id,
            name=data.name,
            event_date=data.event_date,
            event_address=data.event_address,
            event_description=data.event_description
        ))

        return {"message": "EventService created.", "event_service_id": next_id}

    async def update_event_service(self, cnpj: str, event_service_id: int, data: EventServiceUpdate) -> dict:
        
        validate_event_service = await self._validate_event_service(cnpj, event_service_id)
        if not validate_event_service:
            return
        
        validate_ticketModel = await TicketModelService._validate_model(cnpj, data.ticket_model_id)
        if not validate_ticketModel:
            return  

        await database.execute(
            event_service.update()
            .where((event_service.c.cnpj == cnpj) & (event_service.c.event_service_id == event_service_id))
            .values(**data.model_dump())
        )

        return {"message": "EventService updated."}

    async def delete_event_service(self, cnpj: str, event_service_id: int) -> dict:
        validate_event_service = await self._validate_event_service(cnpj, event_service_id)
        if not validate_event_service:
            return

        await database.execute(
            event_service.delete().where(
                (event_service.c.cnpj == cnpj) &
                (event_service.c.event_service_id == event_service_id)
            )
        )

        return {"message": "EventService deleted."}
    
    
    @staticmethod
    async def _validate_event_service(cnpj: str, event_service_id: int):
        event_service_validate = await database.fetch_one(event_service.select().where(
                                                         (event_service.c.cnpj == cnpj) 
                                                       & (event_service.c.event_service_id == event_service_id)
            )
        )
        if not event_service_validate:
            raise HTTPException(status_code=404, detail="EventService not found.")
        
        return event_service_validate