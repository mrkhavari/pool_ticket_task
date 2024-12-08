from passlib.context import CryptContext
from passlib.hash import bcrypt


def get_password_hash(password: str) -> str:
    return str(CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password))
