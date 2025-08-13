from fastapi import HTTPException, status
from sqlalchemy import select
from src.models.login_permission import login_permission
from src.models.permission_type import permission_type
from src.database import database
from src.schemas.login_permission import LoginPermissionIn, LoginPermissionUpdate
from databases.interfaces import Record

class LoginPermissionService:

    async def create_login_permission(self, cnpj: str, data: LoginPermissionIn) -> dict:
        # Verifica se o permission_type existe
        query_check_permission = select(permission_type.c.permission_type).where(
            (permission_type.c.cnpj == cnpj) &
            (permission_type.c.permission_type == data.permission_type)
        )
        if not await database.fetch_one(query_check_permission):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission type not found.")

        await database.execute(login_permission.insert().values(
            cnpj=cnpj,
            email=data.email,
            password=data.password,  # Aqui você pode aplicar hash se quiser
            name=data.name,
            permission_type=data.permission_type
        ))

        return {"message": "LoginPermission created.", "email": data.email}

    async def update_login_permission(self, cnpj: str, email: str, data: LoginPermissionUpdate) -> dict:
        query = login_permission.update().where(
            (login_permission.c.cnpj == cnpj) &
            (login_permission.c.email == email)
        ).values(
            password=data.password,
            name=data.name,
            permission_type=data.permission_type
        )

        result = await database.execute(query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LoginPermission not found.")

        return {"message": "LoginPermission updated."}

    async def delete_login_permission(self, cnpj: str, email: str) -> dict:
        query = login_permission.delete().where(
            (login_permission.c.cnpj == cnpj) &
            (login_permission.c.email == email)
        )
        result = await database.execute(query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LoginPermission not found.")

        return {"message": "LoginPermission deleted."}

    async def read_login_permissions(self, cnpj: str) -> list[Record]:
        query = login_permission.select().where(login_permission.c.cnpj == cnpj)
        return await database.fetch_all(query)
