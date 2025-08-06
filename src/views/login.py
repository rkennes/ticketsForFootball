from pydantic import BaseModel, EmailStr

class LoginAuth(BaseModel):
    cnpj: str
    email: EmailStr
    password: str
