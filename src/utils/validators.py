import re

def is_valid_cnpj(cnpj: str) -> bool:
    return is_not_empty(cnpj) and cnpj.isdigit() and len(cnpj) == 14

def is_valid_email(email: str) -> bool:
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return is_not_empty(email) and re.match(email_regex, email) is not None

def is_valid_password(password: str) -> bool:
    return is_not_empty(password) and len(password) >= 8

def is_valid_corporate_name(corporate_name: str) -> bool:
    return is_not_empty(corporate_name)

def is_not_empty(value: str) -> bool:
    return bool(value and value.strip())