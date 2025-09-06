from pydantic import BaseModel
import datetime


class SignupResponse(BaseModel):
    name: str
    email: str
    created_at: datetime.datetime
    class Config:
        form_attribute = True    