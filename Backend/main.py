from fastapi import FastAPI,Depends
from fastapi.exceptions import HTTPException
from Schemas import UserModels
from Config.database import engine,get_db
from sqlalchemy.orm import Session
from Router.Authentication_route import routes
from Utils import Oauth2
from Utils.Response_model import TokenData



app = FastAPI(
    title = "NUML Insigtbot",
    description = """ This is the backend of NUML Insightbot where 
    user can pass their query directly to the chatbot instead of scrolling
    the website many hours you just pass the query and Chatbot will gave
    you response in a few neno-seconds will real time chat streaming. If you really
    want the API's of this system.you can directly reach out to me at:
    'warishayat666@gmail.com' and i will provide you the detail about it.
    if you like this project please hit the follow button on Github and follow me
    on Linkedin, Some more SAAS projects are on the way.""",
    version = "1.1.0"
)

UserModels.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return{
        "success" : True,
        "message" : "You are looking for pong"
    }

@app.get("/testdatabase")
async def testdatabase(db:Session=Depends(get_db)):
    return{
        "Success" : True,
        "message" : "Successfully....Database is up"
    }
    
@app.get("/dashboard")
def get_dashboard(current_user: TokenData = Depends(Oauth2.get_current_user)):
    return {
        "message": "Welcome to your dashboard!",
        "current_user": {
            "id": current_user.id,
        }
    }
#Signup
app.include_router(routes)