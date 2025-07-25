from fastapi import  status, APIRouter, Depends
from src.schemas.ticket_model import TicketModelIn,TicketModelUpdate,TicketModelSectorIn
from src.views.ticket_model import ticketModelOut
from src.services.ticket_model import TicketModelService


router = APIRouter(prefix="/ticket_model")

service = TicketModelService()

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_ticketModel(data: TicketModelIn):
    return await service.create_ticketModel(data)

@router.get("/{cnpj}", response_model=list[ticketModelOut])
async def read_ticketModel(cnpj: str, limit: int, skip: int = 0):
    return await service.read_ticketModel(cnpj, limit, skip)

@router.delete("/{cnpj}/{ticket_model_id}")
async def delete_model(cnpj: str, ticket_model_id: int):
    return await service.delete_ticket_model(cnpj, ticket_model_id)

@router.delete("/{cnpj}/{ticket_model_id}/sector/{sector_id}")
async def delete_sector(cnpj: str, ticket_model_id: int, sector_id: int):
    return await service.delete_sector_from_model(cnpj, ticket_model_id, sector_id)

@router.put("/{cnpj}/{ticket_model_id}", status_code=status.HTTP_200_OK)
async def update_ticket_model(cnpj: str, ticket_model_id: int, payload: TicketModelUpdate):
    return await service.update_ticket_model(cnpj, ticket_model_id, payload)

@router.post("/{cnpj}/{ticket_model_id}/sector", status_code=status.HTTP_201_CREATED)
async def add_sectors(cnpj: str, ticket_model_id: int, payload: list[TicketModelSectorIn]):
    return await service.add_sectors_to_model(cnpj, ticket_model_id, payload)