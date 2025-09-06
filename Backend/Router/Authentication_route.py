from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from Config.database import get_db
from Middleware.UserValidation import SignupValidation
from Schemas.UserModels import AuthenticationModel
from Utils.Oauth2 import hashPassword
from Utils.Response_model import SignupResponse

routes = APIRouter(
    prefix="/authentication", 
    tags=["login/signup"] 
)

@routes.post("/signup", response_model=SignupResponse) 
async def signup_user(data: SignupValidation, db: Session = Depends(get_db)):  
    existUser = db.query(AuthenticationModel).filter(
        AuthenticationModel.email == data.email  
    ).first()
    
    if existUser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,  
            detail="User already exists"
        )
    
    new_user = AuthenticationModel(
        name=data.name,
        email=data.email,
        password=hashPassword(data.password)  
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user