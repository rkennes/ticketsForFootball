from fastapi import APIRouter
from src.schemas.login import LoginIn
from src.views.login import LoginAuth
from src.services.login import LoginService

router = APIRouter()
service = LoginService()

@router.post("/register")
async def register(data: LoginIn):
    return await service.create_login(data)

@router.post("/login")
async def login(data: LoginAuth):
    return await service.validate_login(data)
