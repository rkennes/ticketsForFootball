from fastapi import  status, APIRouter, Depends
from src.schemas.sector import sectorIn
from src.views.sector import sectorOut
from src.services.sector import SectorService


router = APIRouter(prefix="/sector")

service = SectorService()

@router.post("", response_model=sectorOut, status_code=status.HTTP_201_CREATED)
async def create_sector(data: sectorIn):
    return await service.create_sector(data)

@router.delete("/{cnpj}/{sector_id}", status_code=status.HTTP_200_OK)
async def delete_account(cnpj: str, sector_id: int):
    return await service.delete_sector(cnpj, sector_id)

@router.get("/{cnpj}", response_model=list[sectorOut])
async def read_sectors(cnpj: str, limit: int, skip: int = 0):
    return await service.read_sectors(cnpj, limit, skip)

@router.put("/{sector_id}", status_code=status.HTTP_200_OK)
async def update_sector(sector_id: int, data: sectorIn):
    return await service.update_sector(sector_id, data)
