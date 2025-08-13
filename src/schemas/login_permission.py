from pydantic import BaseModel
from datetime import datetime

class LoginPermissionIn(BaseModel):
    email: str
    password: str
    name: str
    permission_type: int

class LoginPermissionUpdate(BaseModel):
    password: str
    name: str
    permission_type: int

class LoginPermissionOut(BaseModel):
    cnpj: str
    email: str
    name: str
    permission_type: int
    created_at: datetime