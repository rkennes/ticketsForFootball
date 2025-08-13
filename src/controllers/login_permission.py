from fastapi import APIRouter, Depends
from src.schemas.login_permission import LoginPermissionIn, LoginPermissionUpdate
from src.views.login_permission import LoginPermissionOut
from src.services.login_permission import LoginPermissionService
from security import login_required
from src.utils.helper import get_current_cnpj

router = APIRouter(prefix="/login_permission", dependencies=[Depends(login_required)])
service = LoginPermissionService()

@router.get("", response_model=list[LoginPermissionOut])
async def read_login_permissions(cnpj: str = Depends(get_current_cnpj)):
    return await service.read_login_permissions(cnpj)

@router.post("", response_model=dict)
async def create_login_permission(data: LoginPermissionIn, cnpj: str = Depends(get_current_cnpj)):
    return await service.create_login_permission(cnpj, data)

@router.put("/{email}", response_model=dict)
async def update_login_permission(email: str, data: LoginPermissionUpdate, cnpj: str = Depends(get_current_cnpj)):
    return await service.update_login_permission(cnpj, email, data)

@router.delete("/{email}", response_model=dict)
async def delete_login_permission(email: str, cnpj: str = Depends(get_current_cnpj)):
    return await service.delete_login_permission(cnpj, email)
