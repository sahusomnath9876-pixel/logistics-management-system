from app.models import Customers, CustomerCart
from app.database import SessionLocal
from sqlalchemy import select


class CustomerRepo:
    def __init__(self):
        self.__cs_db = Customers
        self.__db = SessionLocal()

    def create_customer(self, **customer):
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

    def get_customer(self, customer_id):
        try:
            if customer_id:
                customer_data = self.__db.get(self.__cs_db, customer_id)

        except Exception:
            return None
        else:
            return customer_data

    def update_customer(self, customer_id, column_name, new_data):
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

    def delete_customer(self, customer_id):
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
    def add_customer(self, user_id, city, address=None):
        new_customer= self.customer_db.create_customer(
            user_id= user_id,
            city= city,
            address= address
            )
        if new_customer:
            return new_customer.get("user_id")

    
class CartRepo:
    def __init__(self):
        self.cart_db = CustomerCart
        self.db = SessionLocal()

    def get_cart(self, customer_id):
        stmt = select(self.cart_db).where(self.cart_db.customer_id == customer_id)
        results = self.db.scalars(stmt).all()
        if results:
            return results

    def assign_warehouse(self, customer_id):
        cart_data = self.get_cart(customer_id)
        if cart_data:
            for data in cart_data:
                data.product_id


    def add_cart(self, customer_id, product_id, qunatity, total_price):
        try:
            new_cart = self.cart_db(
                customer_id= customer_id,
                product_id= product_id,
                qunatity= qunatity,
                total_price= total_price
            )
            self.db.add(new_cart)
            self.db.commit()
            self.db.refresh()

        except Exception as e:
            self.db.rollback()
            return("Error", e)

        else:
            return product_id

    def delete_cart(self, customer_id):
        try:
            cart = self.get_cart(customer_id)
            for data in cart:
                if data:
                    self.db.delete(data)
                    self.db.commit()
        except Exception:
                self.db.rollback()
                return "Error"
        else:
            return customer_id



    def remove_cart(self, id):
        try:
            cart_data = self.db.get(self.cart_db, id)
            if cart_data:
                self.db.delete(cart_data)
                self.db.commit()
                return id
        except Exception:
            self.db.rollback()
            return "Error"
    
            
               



            