from app.repositories import UserRepo, CustomerRepo, AgentRepo, WarehouseRepo, ManagersRepo
import bcrypt
from typing import Any
from app.exceptions import InvalidCerdiantials, NotFoundError, UnexpectedErrorAccuerd, AlreadyExistsError, logger
import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

load_dotenv()

class Authentication:
    def __init__(self, db):
        self.__user_db = UserRepo(db)
        self.__customer_db = CustomerRepo(db)
        self.__manager_db = ManagersRepo(db)
        self.__agent_db = AgentRepo(db)
        self.__warehouse_db = WarehouseRepo(db)


    def user_signUp(self, name : str, mobile_no : str, password : str, city : str) -> object:
    
            try:
                
                name = str(name).title()
                mobile_no = str(mobile_no)
                if len(mobile_no) != 10:
                    raise InvalidCerdiantials("Invalid Mobile Number")                    
                password = str(password)
                #as of now we only support customer registration deliovery agent and warehouse manager will added as soon as possible

                hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()
                get_type = "mobile_no"
                user_data = self.__user_db.get_user(get_type, mobile_no)
                if not user_data:
                    new_user = self.__user_db.create_user(
                        name= name,
                        mobile_no= mobile_no,
                        password= hashed_password,
                        role= "Customer",
                    )
                    if new_user: # transaction handling need as of now im doing manually later we'will upgrade
                        user_data = self.__user_db.get_user(get_type, mobile_no)
                        create_customer = self.__customer_db.add_customer(user_data.user_id, city)
                        if not create_customer:
                            delete_user = self.__user_db.delete_user(user_data.user_id)
                            raise UnexpectedErrorAccuerd("Unable To Complete This SignUp")
                        else:
                            return user_data
                    

                    else:
                        raise UnexpectedErrorAccuerd("Unable To Complete This SignUP ")
                else:
                    raise AlreadyExistsError("User Already Exists")
                    
            except (TypeError, ValueError):
                logger.exception("Invalid Data Type")
                raise                          
                
    def agent_signUp(self, name : str, mobile_no : str, password : str, wearehouse_id : int, vehicle_no : str) -> object: #warehouse_must need to accept this for acess registration
            try:
                
                name = str(name).title()
                mobile_no = str(mobile_no)
                if len(mobile_no) != 10:
                    raise InvalidCerdiantials("Invalid Mobile Number")                   
                password = str(password)
                wearehouse_id = int(wearehouse_id)
                warehouse_data = self.__warehouse_db.get_warehouse(wearehouse_id)
                if not warehouse_data: 
                    raise NotFoundError("Invalid Warehouse Id")
                vehicle_no = str(vehicle_no)

                hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

                get_type = "mobile_no"
                user_data = self.__user_db.get_user(get_type, mobile_no)
                if not user_data:
                    new_user = self.__user_db.create_user(
                        name= name,
                        mobile_no= mobile_no,
                        password= hashed_password,
                        role= "Agent",
                    )
                    if new_user:
                        user_data = self.__user_db.get_user(get_type, mobile_no)
                        create_agent = self.__agent_db.add_agent(user_data.user_id, wearehouse_id, vehicle_no)
                        if not create_agent:
                            delete_user = self.__user_db.delete_user(user_data.user_id)
                            raise UnexpectedErrorAccuerd("Unbale To SignUp At This Moment..")                          
                        else:
                            return user_data
                    

                    else:
                        raise UnexpectedErrorAccuerd("Unbale To SignUp At This Moment..")
                else:
                    raise AlreadyExistsError("User Already Exists")
                    
            except (TypeError, ValueError):
                logger.exception("Invalid Data Type")
                raise

    def manager_signUP(self, name : str, mobile_no : str, password : str, wearehouse_id : int, manager_id : int) -> object:

        try:
            name = str(name)
            mobile_no = str(mobile_no)
            if len(mobile_no) != 10:
                raise InvalidCerdiantials("Invalid Mobile Number") 
            password = str(password)
            wearehouse_id = int(wearehouse_id)
            manager_id = int(manager_id)

            user_data = self.__user_db.get_user("mobile_no", mobile_no)
            if not user_data:
                hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()
                warehouse_data = self.__warehouse_db.get_warehouse(wearehouse_id)
                if warehouse_data and warehouse_data.manager_id == manager_id:
                    create_user = self.__user_db.create_user(
                        name= name, 
                        mobile_no= mobile_no,
                        password= hashed_password,
                        role= "Manager"                        
                    )
                    if create_user:
                        user_data = self.__user_db.get_user("mobile_no", mobile_no)
                        manager = self.__manager_db.add_manager(manager_id, wearehouse_id, user_data.user_id)
                        if not manager:
                            delete_user = self.__user_db.delete_user(user_data.user_id)
                            raise UnexpectedErrorAccuerd("Unbale To SignUp At This Moment..")
                        else:
                            return user_data
                    else:
                        raise UnexpectedErrorAccuerd("Unbale To SignUp At This Moment..")
                else:
                    raise InvalidCerdiantials("Invalid Warehouse Id or Manager Id") 
            else:
                raise AlreadyExistsError("User Already Exists")
        except (TypeError, ValueError):
            logger.exception("Invalid Data Type")
            raise

    def signIN(self, mobile_no : str, password : str) -> object:
        try:
            mobile_no = str(mobile_no)
            if len(mobile_no) != 10:
                raise InvalidCerdiantials("Invalid Mobile Number") 
            auth_type = "mobile_no"
            user_data = self.__user_db.get_user(auth_type, mobile_no)
            if not user_data:
                raise NotFoundError("User Not Exists Or Invalid Mobile No.")
                
            hashed_password = user_data.password

            if bcrypt.checkpw(password.encode(), hashed_password.encode("utf-8")):
                return user_data
            else:
                raise InvalidCerdiantials("Invalid Password")
            
        except (TypeError, ValueError):
            logger.exception("Invalid Data Type")
            raise
            

    def create_auth_token(self, user : object):
        if user.role == "Customer":

            customer = user.customer
            expiry_time = datetime.now(timezone.utc) + timedelta(minutes=10)
            payload = {
                "sub" : "Authentication",
                "user_id" : user.user_id,
                "customer_id" : customer.customer_id,
                "role" : user.role,
                "exp" : expiry_time
            }

            token = jwt.encode(
                payload,
                os.getenv("SECRET_KEY"),
                os.getenv("ALGORITHAM")
            )
            return token
        elif user.role == "Manager":
            manager = user.manager
            expiry_time = datetime.now(timezone.utc) + timedelta(minutes=10)
            payload = {
                "sub" : "Authentication",
                "user_id" : user.user_id,
                "warehouse_id" : manager.warehouse_id,
                "manager_id" : manager.manager_id,
                "role" : user.role,
                "exp" : expiry_time
            }

            token = jwt.encode(
                payload,
                os.getenv("SECRET_KEY"),
                os.getenv("ALGORITHAM")
            )
            return token


Oauth2_password = OAuth2PasswordBearer("/auth/signin")
def verify_token(current_user = Depends(Oauth2_password)):
    payload = jwt.decode(
        current_user,
        os.getenv("SECRET_KEY"),
        os.getenv("ALGORITHAM")        
    )
    return payload


def verify_role(role : str):
    def check_user(user = Depends(verify_token)):
        if user.get("role") != role:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized"
            )
        return user
        
    return check_user                  