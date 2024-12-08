from passlib.context import CryptContext


def verify_password(password: str, hashed_password: str) -> bool:
    return bool(
        CryptContext(schemes=["bcrypt"], deprecated="auto").verify(
            password,
            hashed_password,
        ),
    )
