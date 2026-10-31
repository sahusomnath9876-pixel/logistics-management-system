from app.models import Customers, CustomerCart
from app.database import SessionLocal
from sqlalchemy import select
from typing import Any


class CustomerRepo:
    def __init__(self):
        self.__cs_db = Customers
        self.__db = SessionLocal()

    def create_customer(self, **customer : Any) -> object | None:
        try:
            new_customer = self.__cs_db(**customer)

            self.__db.add(new_customer)
            self.__db.commit()
            self.__db.refresh(new_customer)

        except Exception:
            self.__db.rollback()
            return None
        else:
            return customer

    def get_customer(self, customer_id : int) -> object | None:
        try:
            if customer_id:
                customer_data = self.__db.get(self.__cs_db, customer_id)

        except Exception:
            return None
        else:
            return customer_data

    def update_customer(self, customer_id : int, column_name : str, new_data : str) -> str | None:
        if customer_id:
            try:
                custome_data = self.get_customer(customer_id)
                if custome_data:

                    if column_name.lower() == "address":
                        self.__cs_db.address = new_data
                        self.__db.commit()
                    elif column_name.lower() == "city":
                        self.__cs_db.city = new_data
                        self.__db.commit()


            except Exception:
                self.__db.rollback()
                return None
            else:
                return column_name

    def delete_customer(self, customer_id : int) -> int | None:
        if customer_id:
            try:            
                customer_data = self.get_customer(customer_id)
                if customer_data:
                    self.__db.delete(customer_data)
                    self.__db.commit()

            except Exception:
                self.__db.rollback()
                return None
            else:
                return customer_id
    def add_customer(self, user_id : int, city : str, address : str | None = None) -> int | None:
        new_customer= self.create_customer(
            user_id= user_id,
            city= city,
            address= address
            )
        if new_customer:
            return new_customer.get("user_id")

    
class CartRepo:
    def __init__(self):
        self.__cart_db = CustomerCart
        self.__db = SessionLocal()

    def get_cart(self, customer_id : int) -> object | None:
        stmt = select(self.__cart_db).where(self.__cart_db.customer_id == customer_id)
        results = self.__db.scalars(stmt).all()
        if results:
            return results

    def assign_warehouse(self, customer_id : int) -> int | None:
        cart_data = self.get_cart(customer_id)
        if cart_data:
            for data in cart_data:
                data.product_id


    def add_cart(self, customer_id : int, product_id : int, qunatity : int, total_price : int) -> int | None:
        try:
            new_cart = self.__cart_db(
                customer_id= customer_id,
                product_id= product_id,
                qunatity= qunatity,
                total_price= total_price
            )
            self.__db.add(new_cart)
            self.__db.commit()
            self.__db.refresh()

        except Exception as e:
            self.__db.rollback()
            return("Error", e)

        else:
            return product_id

    def delete_cart(self, customer_id : int) -> int | None:
        try:
            cart = self.get_cart(customer_id)
            for data in cart:
                if data:
                    self.__db.delete(data)
                    self.__db.commit()
        except Exception:
                self.__db.rollback()
                return None
        else:
            return customer_id



    def remove_cart(self, id : int) -> int | None:
        try:
            cart_data = self.__db.get(self.__cart_db, id)
            if cart_data:
                self.__db.delete(cart_data)
                self.__db.commit()
                return id
        except Exception:
            self.__db.rollback()
            return None