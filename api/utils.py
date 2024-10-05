from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_passwd(plaintext_passwd: str, hashed_passwd: str):
    return pwd_context.verify(plaintext_passwd, hashed_passwd)