from fastapi import APIRouter, Depends
from src.schemas.permission_type import PermissionTypeIn, PermissionTypeUpdate
from src.views.permission_type import PermissionTypeOut
from src.services.permission_type import PermissionTypeService
from security import login_required
from src.utils.helper import get_current_cnpj

router = APIRouter(prefix="/permission_type", dependencies=[Depends(login_required)])
service = PermissionTypeService()

@router.get("", response_model=list[PermissionTypeOut])
async def read_permission_types(cnpj: str = Depends(get_current_cnpj)):
    return await service.read_permission_types(cnpj)

@router.post("", response_model=dict)
async def create_permission_type(data: PermissionTypeIn, cnpj: str = Depends(get_current_cnpj)):
    return await service.create_permission_type(cnpj, data)

@router.put("/{permission_type_id}", response_model=dict)
async def update_permission_type(permission_type_id: int, data: PermissionTypeUpdate, cnpj: str = Depends(get_current_cnpj)):
    return await service.update_permission_type(cnpj, permission_type_id, data)
