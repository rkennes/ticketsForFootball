from pydantic import BaseModel, EmailStr

class LoginAuth(BaseModel):
    email: EmailStr
    password: str
