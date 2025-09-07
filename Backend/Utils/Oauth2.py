from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from datetime import datetime,timedelta
from jose import JWTError,jwt
from Utils.Response_model import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status

Oauth_Scheme = OAuth2PasswordBearer(tokenUrl="/authentication/login")
load_dotenv()

Algoritham = os.getenv("ALGORITHM")
Secret = os.getenv("SECRET_KEY")
Access_token_Expire = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


pwd_context =  CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashPassword(password:str):
    return pwd_context.hash(password)


def decodePassword(plain_pass,hash_pass):
    return pwd_context.verify(plain_pass,hash_pass)



def create_acces_token(payload:dict):
    data = payload.copy()
    EXPIRE = datetime.utcnow() + timedelta(minutes=int(Access_token_Expire))
    data.update({"exp":EXPIRE})
    jwt_token = jwt.encode(data,Secret, algorithm=Algoritham)
    return jwt_token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, Secret, algorithms=[Algoritham])
        user_id = payload.get("user_id")
        if not user_id:
            raise credentials_exception
        token_data=TokenData(id=user_id)
        return token_data
    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(Oauth_Scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not authenticate user credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)