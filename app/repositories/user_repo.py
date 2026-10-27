from app.models import Users, DeliveryAgent
from app.database import SessionLocal
from sqlalchemy import select
from typing import Any

class UserRepo:
    def __init__(self):
        self.__user_db = Users
        self.__db = SessionLocal()


    def get_user(self, get_type : str, type_data : Any) -> object | None:  #user can be get through his mobile number

        try:
            user_data = None
            if get_type.lower() == "mobile_no":
                mobile_no = type_data
                stmt = select(self.__user_db).where(self.__user_db.mobile_no == mobile_no)
                result = self.__db.scalars(stmt).all()

                for data in result:
                    user_data = data
                    
            elif get_type.lower() == "user_id":
                user_id = type_data
                result = self.__db.get(self.__user_db, user_id)
                user_data = result
        except Exception:
            return None
        else:
            return user_data

    def create_user(self, **user_info : Any) -> object | None:
        if user_info:
            new_user = self.__user_db(**user_info)
            try:
                self.__db.add(new_user)
                self.__db.commit()
                self.__db.refresh(new_user)

            except Exception:
                self.__db.rollback()
                return None
            else:
                return user_info

    def update_user(self, user_id : int, column_name : str, new_data : Any) -> str | None:
        if user_id:
            try:
                user_data = self.__db.get(self.__user_db, user_id)
                if user_data:

                    if column_name.lower() == "password":
                        user_data.password = new_data
                        self.__db.commit()
                    elif column_name.lower() == "mobile_no":
                        user_data.mobile_no = new_data
                        self.__db.commit()
                    elif column_name.lower() == "name":
                        user_data.name = new_data
                        self.__db.commit()

            except Exception:
                self.__db.rollback()
                return None
            else:
                return column_name

    def delete_user(self, user_id : int) -> int | None:
        if user_id:
            try: 
                user_data = self.__db.get(self.__user_db, user_id)

                self.__db.delete(user_data)
                self.__db.commit()
            except Exception:
                self.__db.rollback()
                return None
            else:
                return user_id


class AgentRepo:
    def __init__(self):
        self.__db = SessionLocal()
        self.__agent = DeliveryAgent

    def get_agent(self, agent_id : int) -> object | None:
        return self.__db.get(self.__agent, agent_id)

    def create_agent(self, **agent_details : Any) -> object | None:
        try:
            new_agent = self.__agent(**agent_details)

            self.__db.add(new_agent)
            self.__db.commit()
            self.__db.refresh(new_agent)

        except Exception:
            self.__db.rollback()
            return None
        else:
            return agent_details

    def update_avaivality(self, agent_id : int, avaivality : bool) -> int | None:
        try:
            agent_data = self.get_agent(agent_id)

            if agent_data:
                agent_data.avaivility = avaivality
                self.__db.commit()

        except Exception:
            self.__db.rollback()
            return None
        else:
            return agent_id

    def delete_agent(self, agent_id : int) -> int | None:
        try:
            agent_data = self.get_agent(agent_id)
            if agent_data:
                self.__db.delete(agent_data)
                self.__db.commit()

        except Exception:
            self.__db.rollback()
            return None
        else:
            return agent_id

    def add_agent(self, user_id : int, warehouse_id : int, vehicle_no : str) -> int:

            new_agent = self.agent_db.create_agent(
                user_id= user_id,
                warehouse_id= warehouse_id,
                vehicle_no= vehicle_no
            )  
            if new_agent:
                return new_agent.get("user_id")


        

                
                
    


                


            



        
