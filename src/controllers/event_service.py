from fastapi import APIRouter, Depends
from src.schemas.event_service import EventServiceIn, EventServiceUpdate
from src.views.event_service import EventServiceOut
from src.services.event_service import EventService
from security import login_required
from src.utils.helper import get_current_cnpj

router = APIRouter(prefix="/event_service", dependencies=[Depends(login_required)])

service = EventService()

@router.get("", response_model=list[EventServiceOut])
async def read_event_service(cnpj: str = Depends(get_current_cnpj)):
    return await service.read_event_service(cnpj)

@router.post("", response_model=dict)
async def create_event_service(data: EventServiceIn, cnpj: str = Depends(get_current_cnpj)):
    return await service.create_event_service(data, cnpj)

@router.put("/{event_service_id}", response_model=dict)
async def update_event_service(event_service_id: int, data: EventServiceUpdate, cnpj: str = Depends(get_current_cnpj)):
    return await service.update_event_service(cnpj, event_service_id, data)

@router.delete("/{event_service_id}", response_model=dict)
async def delete_event_service(event_service_id: int, cnpj: str = Depends(get_current_cnpj)):
    return await service.delete_event_service(cnpj, event_service_id)
