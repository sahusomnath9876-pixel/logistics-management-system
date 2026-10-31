from app.repositories import UserRepo, CustomerRepo, AgentRepo, WarehouseRepo, ManagersRepo
import bcrypt
from typing import Any


class Authentication:
    def __init__(self):
        self.__user_db = UserRepo()
        self.__customer_db = CustomerRepo()
        self.__manager_db = ManagersRepo()
        self.__agent_db = AgentRepo()
        self.__warehouse_db = WarehouseRepo()


    def user_signUp(self, name : str, mobile_no : str, password : str, city : str) -> dict[str, Any]:
            if not (name and mobile_no and password and city):
                return{"success" : False, "message" : "User Alreday Exists", "user" : None}
    
            try:
                
                name = str(name).title()
                mobile_no = str(mobile_no)
                if len(mobile_no) != 10:
                    return{"success" : False, "message" : "Invalid Mobile Number Length", "user" : None}                    
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
                            return{"success" : False, "message" : "Error", "user" : None}
                        else:
                            return{"success" : True, "message" : "Registerd Successfuly", "user" : user_data.user_id}
                    

                    else:
                        return{"success" : False, "message" : "Error", "user" : None}
                else:
                    return{"success" : False, "message" : "User Alreday Exists", "user" : None}
                    
            except TypeError:
                return{"success" : False, "message" : "Invalid Data Type", "user" : None}
            except Exception as e:
                return{"success" : False, "message" : f"Error{e}", "user" : None}
                
    def agent_signUp(self, name : str, mobile_no : str, password : str, wearehouse_id : int, vehicle_no : str) -> dict[str, Any]: #warehouse_must need to accept this for acess registration
            if not (name and mobile_no and password and wearehouse_id and vehicle_no):
                return{"success" : False, "message" : "Fields Required", "user" : None}
    
            try:
                
                name = str(name).title()
                mobile_no = str(mobile_no)
                if len(mobile_no) != 10:
                    return{"success" : False, "message" : "Invalid Mobile Number Length", "user" : None}                    
                password = str(password)
                wearehouse_id = int(wearehouse_id)
                warehouse_data = self.__warehouse_db.get_warehouse(wearehouse_id)
                if not warehouse_data: 
                    return{"success" : False, "message" : "Invalid Warehouse Id", "user" : None}             
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
                            return{"success" : False, "message" : "Error", "user" : None}                           
                        else:
                            return{"success" : True, "message" : "Registerd Successfuly", "user" : user_data.user_id}
                    

                    else:
                        return{"success" : False, "message" : "Error", "user" : None}
                else:
                    return{"success" : False, "message" : "User Alreday Exists", "user" : None}
                    
            except TypeError:
                return{"success" : False, "message" : "Invalid Data Type", "user" : None}
            except Exception as e:
                return{"success" : False, "message" : f"Error{e}", "user" : None}

    def manager_signUP(self, name : str, mobile_no : str, password : str, wearehouse_id : int, manager_id : int) -> dict[str, Any]:
        if not (name and mobile_no and password and wearehouse_id and manager_id):
            return{"success" : False, "message" : "Fields Required", "user" : None}

        try:
            name = str(name)
            mobile_no = str(mobile_no)
            if len(mobile_no) != 10:
                return{"success" : False, "message" : "Invalid Mobile No Length", "user" : None}
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
                        role= "Manger"                        
                    )
                    if create_user:
                        user_data = self.__user_db.get_user("mobile_no", mobile_no)
                        manager = self.manager_db.add_manager(manager_id, wearehouse_id, user_data.user_id)
                        if not manager:
                            delete_user = self.__user_db.delete_user(user_data.user_id)
                            return{"success" : False, "message" : "Error", "user" : None}
                        else:
                            return{"success" : True, "message" : "Registerd Successfuly", "user" : user_data.user_id}
                    else:
                        return{"success" : False, "message" : "Error", "user" : None}
                else:
                    return{"success" : False, "message" : "Invalid Manger or Warehouse Id", "user" : None}
            else:
                return{"success" : False, "message" : "User Already Exists", "user" : None}
        except TypeError:
            return{"success" : False, "message" : "Invalid Data Type", "user" : None}
        except Exception as e:
            return{"success" : False, "message" : f"Error{e}", "user" : None}

    def signIN(self, mobile_no : str, password : str) -> dict[str, Any]:
        if not (mobile_no and password):
            return{"success" : False, "message" : "Fields Required", "user" : None}
        try:
            mobile_no = str(mobile_no)
            if len(mobile_no) != 10:
                return{"success" : False, "message" : "Invalid Mobile Number Length", "user" : None}
            auth_type = "mobile_no"
            user_data = self.__user_db.get_user(auth_type, mobile_no)
            if not user_data:
                return{"success" : False, "message" : "User Not Exists", "user" : None}
                
            hashed_password = user_data.password

            if bcrypt.checkpw(password.encode(), hashed_password.encode("utf-8")):
                return{"success" : True, "message" : "SignIN Successfuly", "user" : user_data}
            else:
                return{"success" : False, "message" : "Invalid Password", "user" : None}
        except TypeError:
            return{"success" : False, "message" : "Invalid Data Type", "user" : None}
        except Exception as e:
            return{"success" : False, "message" : f"Error{e}", "user" : None}
            

                           