from fastapi import Depends
from security import login_required  

def get_current_cnpj(user = Depends(login_required)) -> str:
    return user["cnpj"]