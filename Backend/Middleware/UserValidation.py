from pydantic import BaseModel,EmailStr
from typing import Optional

class SignupValidation(BaseModel):
    name:str
    email:EmailStr
    password:str
    
class LoginValidation(BaseModel):
    email:EmailStr
    password : str

