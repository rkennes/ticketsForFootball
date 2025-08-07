from src.database import database
from src.models.login import login
from src.schemas.login import LoginIn
from src.views.login import LoginAuth
from src.utils.security import hash_password, verify_password
from sqlalchemy import select, and_
from fastapi import HTTPException
from src.utils.validators import is_valid_cnpj, is_valid_password, is_valid_email, is_valid_corporate_name
from security import sign_jwt


class LoginService:
    
    @staticmethod
    def validate_login_informations(data: LoginIn): 
        if not is_valid_cnpj(data.cnpj):
            raise HTTPException(status_code=400, detail="CNPJ invalid.")
                
        if not is_valid_email(data.email):
            raise HTTPException(status_code=400, detail="Email invalid.")
        
        if not is_valid_password(data.password):
            raise HTTPException(status_code=400, detail="Password invalid. Password needs 8 or more caracteres")
        
        if not is_valid_corporate_name(data.corporate_name):
            raise HTTPException(status_code=400, detail="Corporate name invalid.")
        

    async def create_login(self, data: LoginIn) -> dict:
        
        self.validate_login_informations(data)
        
        query = select(login).where(
            (login.c.cnpj == data.cnpj) & (login.c.email == data.email)
        )
        existing = await database.fetch_one(query)
        if existing:
            raise HTTPException(status_code=400, detail="User already registered.")

        values = data.model_dump()
        values["password"] = hash_password(values["password"])

        await database.execute(login.insert().values(**values))
        return {"message": "User registered successful."}

    async def validate_login(self, data: LoginAuth) -> dict:
        query = select(login).where(
            (login.c.cnpj == data.cnpj) & (login.c.email == data.email)
        )
        user = await database.fetch_one(query)
        if not user or not verify_password(data.password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid Credentials.")
        
        return {
            "message": "Login successful",
            "cnpj": user["cnpj"],
            "email": user["email"],
            "corporate_name": user["corporate_name"],
            "access_token": sign_jwt(data.cnpj)
        }
