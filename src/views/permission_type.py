from datetime import datetime
from pydantic import BaseModel

class PermissionTypeOut(BaseModel):
    cnpj: str
    permission_type: int
    description: str
    created_at: datetime
