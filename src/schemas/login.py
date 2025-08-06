from pydantic import BaseModel

class LoginIn(BaseModel):
    cnpj: str
    email: str
    password: str
    corporate_name: str
