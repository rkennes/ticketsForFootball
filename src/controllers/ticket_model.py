from fastapi import  status, APIRouter, Depends
from src.schemas.ticket_model import TicketModelIn,TicketModelUpdate,TicketModelSectorIn
from src.views.ticket_model import ticketModelOut
from src.services.ticket_model import TicketModelService
from security import login_required
from src.utils.helper import get_current_cnpj

router = APIRouter(prefix="/ticket_model", dependencies=[Depends(login_required)])

service = TicketModelService()

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_ticketModel(data: TicketModelIn, cnpj: str = Depends(get_current_cnpj)):
    return await service.create_ticketModel(data, cnpj)

@router.get("", response_model=list[ticketModelOut])
async def read_ticketModel(limit: int, skip: int = 0, cnpj: str = Depends(get_current_cnpj)):
    return await service.read_ticketModel(cnpj, limit, skip)

@router.delete("/{ticket_model_id}")
async def delete_model(ticket_model_id: int, cnpj: str = Depends(get_current_cnpj)):
    return await service.delete_ticket_model(cnpj, ticket_model_id)

@router.delete("/{ticket_model_id}/sector/{sector_id}")
async def delete_sector(ticket_model_id: int, sector_id: int, cnpj: str = Depends(get_current_cnpj)):
    return await service.delete_sector_from_model(cnpj, ticket_model_id, sector_id)

@router.put("/{ticket_model_id}", status_code=status.HTTP_200_OK)
async def update_ticket_model(ticket_model_id: int, payload: TicketModelUpdate, cnpj: str = Depends(get_current_cnpj)):
    return await service.update_ticket_model(cnpj, ticket_model_id, payload)

@router.post("/{ticket_model_id}/sector", status_code=status.HTTP_201_CREATED)
async def add_sectors(ticket_model_id: int, payload: list[TicketModelSectorIn], cnpj: str = Depends(get_current_cnpj)):
    return await service.add_sectors_to_model(cnpj, ticket_model_id, payload)