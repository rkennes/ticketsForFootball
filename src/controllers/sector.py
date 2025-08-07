from fastapi import  status, APIRouter, Depends
from src.schemas.sector import sectorIn
from src.views.sector import sectorOut
from src.services.sector import SectorService
from security import login_required
from src.utils.helper import get_current_cnpj

router = APIRouter(prefix="/sector", dependencies=[Depends(login_required)])

service = SectorService()

@router.post("", response_model=sectorOut, status_code=status.HTTP_201_CREATED)
async def create_sector(data: sectorIn, cnpj: str = Depends(get_current_cnpj)):
    return await service.create_sector(data, cnpj)

@router.delete("/{sector_id}", status_code=status.HTTP_200_OK)
async def delete_account(sector_id: int, cnpj: str = Depends(get_current_cnpj)):
    return await service.delete_sector(sector_id, cnpj)

@router.get("", response_model=list[sectorOut])
async def read_sectors(limit: int, skip: int = 0, cnpj: str = Depends(get_current_cnpj)):
    return await service.read_sectors(cnpj, limit, skip)

@router.put("/{sector_id}", status_code=status.HTTP_200_OK)
async def update_sector(sector_id: int, data: sectorIn, cnpj: str = Depends(get_current_cnpj)):
    return await service.update_sector(sector_id, data, cnpj)
