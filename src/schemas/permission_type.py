from pydantic import BaseModel
from datetime import datetime

class PermissionTypeIn(BaseModel):
    description: str

class PermissionTypeUpdate(BaseModel):
    description: str

class PermissionTypeOut(BaseModel):
    cnpj: str
    permission_type: int
    description: str
    created_at: datetime