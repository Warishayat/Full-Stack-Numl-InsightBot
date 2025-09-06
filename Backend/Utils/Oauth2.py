from passlib.context import CryptContext
pwd_context =  CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashPassword(password:str):
    return pwd_context.hash(password)


def decodePassword(plain_pass,hash_pass):
    return pwd_context.verify(plain_pass,hash_pass)