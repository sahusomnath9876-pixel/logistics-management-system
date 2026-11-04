from pydantic import BaseModel

class Auth(BaseModel):
    user_id : int
    password : str

class SignUp(BaseModel):
    pass