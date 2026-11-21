from app.services import Authentication, verify_token, verify_role
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.database import get_db
from app.repositories import UserRepo
from app.schemas import UserResponse, ManagerSignUp, SignUpResponse, CustomerSignUp, Auth
from app.exceptions import *

router = APIRouter(prefix="/auth", tags=["Authentication"])



@router.post("/signin")
def signin(user : Auth, db=Depends(get_db)):
    auth = Authentication(db)

    user_data = auth.signIN(user.username, user.password)

    create_token = auth.create_auth_token(user_data)
    if not create_token:
        raise InvalidCerdiantials("Invalid Username or Password")

    return{
        "access_token" : create_token,
        "token_type" : "Bearer"
    }


@router.get("/getuser", response_model=UserResponse)
def get_user_data(mobile_no : str, db=Depends(get_db), current_user = Depends(verify_role("Customer"))):

    user = UserRepo(db)

    user_data = user.get_user("mobile_no", mobile_no)
    return user_data


@router.post("/signup/customer", status_code=201, response_model=SignUpResponse)
def customer_signup(new_user : CustomerSignUp, db=Depends(get_db)):
    auth = Authentication(db)


    reg = auth.user_signUp(new_user.name, 
                new_user.mobile_no, new_user.password, new_user.city)
    return reg



@router.post("/signup/manager", status_code=201, response_model=SignUpResponse)
def manager_signup(new_user : ManagerSignUp, db=Depends(get_db)):
    auth = Authentication(db)

    reg = auth.manager_signUP(new_user.name, new_user.mobile_no, new_user.password, new_user.warehouse_id, new_user.manager_id)
    return reg  
