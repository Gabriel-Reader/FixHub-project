import re
from email_validator import validate_email, EmailNotValidError

def validar_email(email):
    """Valida o formato do e-mail"""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def validar_password(password):
    """Valida se a senha tem pelo menos 8 caracteres."""
    return re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$', password) is not None

def validar_username(username):
    """Pelo menos 3 caracteres, letra e números"""
    return re.fullmatch(r'^[a-zA-Z0-9_]{3,20}$', username) is not Non