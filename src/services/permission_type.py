from fastapi import HTTPException, status
from sqlalchemy import select, func
from src.models.permission_type import permission_type
from src.database import database
from src.schemas.permission_type import PermissionTypeIn, PermissionTypeUpdate
from databases.interfaces import Record

class PermissionTypeService:

    async def create_permission_type(self, cnpj: str, data: PermissionTypeIn) -> dict:
        query_max_id = select(func.max(permission_type.c.permission_type)).where(
            permission_type.c.cnpj == cnpj
        )
        last_id = await database.fetch_val(query_max_id) or 0
        next_id = last_id + 1

        await database.execute(permission_type.insert().values(
            cnpj=cnpj,
            permission_type=next_id,
            description=data.description
        ))

        return {"message": "PermissionType created.", "permission_type": next_id}

    async def update_permission_type(self, cnpj: str, permission_type_id: int, data: PermissionTypeUpdate) -> dict:
        query = permission_type.update().where(
            (permission_type.c.cnpj == cnpj) &
            (permission_type.c.permission_type == permission_type_id)
        ).values(description=data.description)

        result = await database.execute(query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PermissionType not found.")

        return {"message": "PermissionType updated."}

    async def read_permission_types(self, cnpj: str) -> list[Record]:
        query = permission_type.select().where(permission_type.c.cnpj == cnpj)
        return await database.fetch_all(query)
