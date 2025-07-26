from fastapi import APIRouter
from src.schemas.event_service import EventServiceIn, EventServiceUpdate
from src.views.event_service import EventServiceOut
from src.services.event_service import EventService

router = APIRouter(prefix="/event_service", tags=["Event Service"])

service = EventService()

@router.get("/{cnpj}", response_model=list[EventServiceOut])
async def read_event_service(cnpj: str):
    return await service.read_event_service(cnpj)

@router.post("/", response_model=dict)
async def create_event_service(data: EventServiceIn):
    return await service.create_event_service(data)

@router.put("/{cnpj}/{event_service_id}", response_model=dict)
async def update_event_service(cnpj: str, event_service_id: int, data: EventServiceUpdate):
    return await service.update_event_service(cnpj, event_service_id, data)

@router.delete("/{cnpj}/{event_service_id}", response_model=dict)
async def delete_event_service(cnpj: str, event_service_id: int):
    return await service.delete_event_service(cnpj, event_service_id)
