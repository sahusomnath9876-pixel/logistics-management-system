from app.services import Authentication, verify_token, verify_role
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.database import get_db
from app.repositories import UserRepo
from app.schemas import UserResponse


router = APIRouter(prefix="/auth", tags=["Authentication"])



@router.post("/signin")
def signin(user : OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    auth = Authentication(db)

    user_data = auth.signIN(user.username, user.password)

    create_token = auth.create_auth_token(user_data)

    return{
        "access_token" : create_token,
        "token_type" : "Bearer"
    }


@router.get("/getuser", response_model=UserResponse)
def get_user_data(mobile_no : str, db=Depends(get_db), current_user = Depends(verify_role("Customer"))):

    user = UserRepo(db)

    user_data = user.get_user("mobile_no", mobile_no)
    return user_data


