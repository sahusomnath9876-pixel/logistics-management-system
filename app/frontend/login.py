from app.services import Authentication

class loginUI:
    def homepage_ui(self):
        
        while True:
            print("-" * 50)
            print("\t\tWelcome to Instacart")
            print("-" * 50)
            print("Options : ")
            print("-" * 50)
            print("1. SignIN\n2. SignUp\n3. Exit")
            option = input("Enter Your Option Here = ")
            if not option:
                print("Option Requierd")
                continue
            try:
                option = int(option)
                return option
            except TypeError:
                print("Invalid Data Type")

    def login_input(self):
        while True:
            mobile_no = input("Enter Your Mobile Number = ").strip()
            if not mobile_no:
                print("Mobile Number Requierd")
                continue
               
            password = input("Enter Your Password = ").strip()
            if not password:
                print("Password Required..")
                continue
            return mobile_no, password

    def user_reg_input(self):
        while True:
            name = input("Enter Your Name Here = ").strip()
            if not name:
                print("Name Field Requierd")
                continue
            mobile_no = input("Enter Your Mobile Number = ").strip()
            if not mobile_no:
                print("Mobile Number Requierd")
                continue
            password = input("Enter Your Password Here = ").strip()
            if not password:
                print("Password Must Requierd")
                continue
            confirm = input("Enter Your Password Again = ").strip()
            if not password:
                print("Password Must Requierd")
                continue
            if password != confirm:
                print("Password isn't matching")
                continue
            city = input("Enter Your City = ").strip()
            if not city:
                print("City Requierd")
                continue
            return name, mobile_no, confirm, city

    def manager_reg_input(self):
        while True:
            name = input("Enter Your Name Here = ").strip()
            if not name:
                print("Name Field Requierd")
                continue
            mobile_no = input("Enter Your Mobile Number = ").strip()
            if not mobile_no:
                print("Mobile Number Requierd")
                continue
            password = input("Enter Your Password Here = ").strip()
            if not password:
                print("Password Must Requierd")
                continue
            confirm = input("Enter Your Password Again = ").strip()
            if not password:
                print("Password Must Requierd")
                continue
            if password != confirm:
                print("Password isn't matching")
                continue
            warehouse_id = int(input("Enter Your City = "))
            if not warehouse_id:
                print("WarehouseId Requierd")
                continue
            manager_id = int(input("Enter Your Manager Id = "))
            if not manager_id:
                print("Manger Id Requierd")
                continue
            return name, mobile_no, confirm, warehouse_id, manager_id
    def role_input(self):
        while True:
            print("1. Customer\n2. Manager\n3. Back")
            role = input("Enter Your Role Option = ")

            try:
                role = int(role)
                return role

            except TypeError:
                print("Invalid Input Type")

class Auth(loginUI):
    def __init__(self):
        self.auth = Authentication()       

    def homepage(self):
        while True:
            option = self.homepage_ui()
            if option == 1:
                mobile_no, password = self.login_input()
                login = self.auth.signIN(mobile_no, password)
                if login.get("success"):
                    print(login.get("message"))
                    return login.get("user")
                else:
                    print(login.get("message"))
            elif option == 2:
                role = self.role_input()
                if role == 1:
                    name, mobile_no, password, city = self.user_reg_input() 
                    new_customer = self.auth.user_signUp(name, mobile_no, password, city) 
                    if new_customer.get("success"):
                        print(new_customer.get("message"))      
                        return new_customer.get("user")
                    else:
                        print(new_customer.get("message"))       
                elif role == 2:
                    name, mobile_no, password, warehouse_id, manager_id = self.manager_reg_input()
                    registration = self.auth.manager_signUP(name, mobile_no, password, warehouse_id, manager_id)
                    if registration.get("success"):
                        print(registration.get("message"))
                        return registration.get("user")
                    else:
                        print(registration.get("message"))
                elif role == 3:
                    continue
            elif option == 3:
                print("Thank You For Visiting Us")
            

                

                             



            

