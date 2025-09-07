from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from Config.database import get_db
from Middleware.UserValidation import SignupValidation,LoginValidation
from Schemas.UserModels import AuthenticationModel
from Utils.Oauth2 import hashPassword,decodePassword
from Utils.Response_model import SignupResponse
from Utils.Oauth2 import create_acces_token
from fastapi.security import OAuth2PasswordRequestForm
from Utils.Response_model import TokenData
from Utils import Oauth2

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


#Implement logic for Login and issuning token of jwt
@routes.post("/login")
async def login_handle(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(AuthenticationModel).filter(
        AuthenticationModel.email == payload.username
    ).first()

    if not user or not decodePassword(hash_pass=user.password, plain_pass=payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Email or password."
        )
    token = create_acces_token(payload={"user_id": user.id})
    return{
       "access_token" : token,
        "token_type" : "bearer"
   }


#get all signup user
@routes.get("/allvaliduser")
def all_valid_user(db:Session=Depends(get_db),current_user: TokenData = Depends(Oauth2.get_current_user)):
    allUsers = db.query(AuthenticationModel).all()
    if not allUsers:
        return HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="NO User found"
        )
    return allUsers