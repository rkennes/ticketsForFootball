from datetime import datetime
from pydantic import BaseModel

class LoginPermissionOut(BaseModel):
    cnpj: str
    email: str
    name: str
    permission_type: int
    created_at: datetime
