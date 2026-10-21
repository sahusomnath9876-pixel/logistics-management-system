from app.models import Orders, OrderItems, Payments
from app.database import SessionLocal
from sqlalchemy import select


class OrdersRepo:
    def __init__(self):
        self.__db = SessionLocal()
        self.__order_db = Orders

    def create_order(self, **order):
        try:
            new_order = self.__order_db(**order)

            self.__db.add(new_order)
            self.__db.commit()
            self.__db.refresh(new_order)

        except Exception as e:
            self.__db.rollback()
            return e
        else:
            return new_order

    def get_order(self, order_id):
        if order_id:
            try:
                order_data = self.__db.get(self.__order_db, order_id)

            except Exception:
                return None
            else:
                return order_data

    def update_status(self, order_id, updated_type, updated_data):
        if updated_data:
            updated_type = str(updated_type).lower()
            try:
                order_data = self.get_order(order_id)
                if order_data:
                    if updated_type == "status":
                        order_data.status = updated_data
                        self.__db.commit()
                    elif updated_type == "amount":
                        order_data.total_amount = updated_data
                        self.__db.commit()
                    elif updated_type == "payment":
                        order_data.payment = updated_data
                        self.__db.commit()
                    
            except TypeError:
                return None  
            except Exception:
                self.__db.rollback()
                return None
            else:
                return order_data.order_id
    def delete_order(self, order_id):
        if order_id:
            try:
                order_data = self.get_order(order_id)
                if order_data:
                    self.__db.delete(order_data)
                    self.__db.commit()
            except Exception:
                self.__db.rollback()
                return None
            else:
                return order_id

    def get_customer_order(self, customer_id):
        try:
            stmt = select(self.__order_db).where(self.__order_db.customer_id == customer_id)
            result = self.__db.scalars(stmt).all()
            if result:
                return result

        except Exception:
            return None

#need to add delete if user deleted his id permenantly then we'will implement it later...

class OItemsRepo:
    def __init__(self):
        self.__db = SessionLocal()
        self.__order_items = OrderItems

    def create_order_items(self, **order_items):
        try:
            new_order_items = self.__order_items(**order_items)

            self.__db.add(new_order_items)
            self.__db.flush()
            self.__db.refresh(new_order_items)
            return new_order_items
        except Exception as e:
            self.__db.rollback()
            return f"Error{e}"
                  
    def show_pending_orders(self, warehouse_id):
        try:
            stmt = select(self.__order_items).where(self.__order_items.assigned_warehouse == warehouse_id, self.__order_items.current_status == "Order Placed")
            results = self.__db.scalars(stmt).all()
            if results:
                return results
        except Exception:
            self.__db.rollback()
            return None


    def get_order_items(self, order_id):
        if id:
            try:
                stmt = select(self.__order_items).where(self.__order_items.order_id == order_id)
                result = self.__db.scalars(stmt).all()
                if result:
                    for data in result:
                        return data.id
        

            except Exception:
                return None
    def fetch_order_items(self, order_id):
        if id:
            try:
                stmt = select(self.__order_items).where(self.__order_items.order_id == order_id)
                result = self.__db.scalars(stmt).all()
                if result:
                    return result
            except Exception:
                return None

    def assign_warehouse(self, oi_id, warehouse_id):
        try:
            stmt = select(self.__order_items).where(self.__order_items.id == oi_id, self.__order_items.assigned_warehouse.is_(None))
            data = self.__db.scalars(stmt).first()

            if data:
                data.assigned_warehouse = warehouse_id
                self.__db.commit()
                return oi_id
        except Exception as e:
            self.__db.rollback()
            return "Error", e



    def update_order_items(self, id, date):
        try:
            order_items = self.__db.get(self.__order_items, id)
            if order_items:
         
                order_items.expected_delivery = date
                self.__db.commit()
                return id
        except Exception as e:
            self.__db.rollback()
            return f"Error{e}"

        
    def update_status(self, order_id, updated_type, updated_data):
        if updated_data:
            updated_type = str(updated_type).lower()
            try:
                stmt = select(self.__order_items).where(self.__order_items.order_id == order_id)
                order_data = self.__db.scalars(stmt).all()
                if order_data:
                    for data in order_data:
                        if updated_type == "status":
                            data.current_status= updated_data
                            self.__db.commit()
                        elif updated_type == "amount":
                            data.assigned_warehouse = updated_data
                            self.__db.commit()
                    
            except TypeError:
                return None  
            except Exception as e:
                self.__db.rollback()
                return None
            else:
                return data.order_id  
    def update_current_status(self, id, new_status):
        try:
            data = self.__db.get(self.__order_items, id)
            if data:
                data.current_status = new_status
                self.__db.commit()
                return id
                
        except Exception:
            self.__db.rollback()
            return None               
            


class PaymentsRepo:
    def __init__(self):
        self.__db = SessionLocal()
        self.__pay_db = Payments

    def create_transaction(self, **pay_details):
        try:
            new_transaction = self.__pay_db(**pay_details)

            self.__db.add(new_transaction)
            self.__db.commit()
            self.__db.refresh(new_transaction)
            return new_transaction

        except Exception:
            self.__db.rollback()
            return None


    def get_transaction(self, txn_id):
        if txn_id:
            try:
                txn_data = self.__db.get(self.__pay_db, txn_id)

            except Exception:
                return None
            else:
                if txn_data:
                    return txn_data

    def delete_transaction(self, txn_id):
        try:
            txn_data = self.get_transaction(txn_id)
            if txn_data:
                self.__db.delete(txn_data)
                self.__db.commit()

        except Exception:
            return None
        else:
            return txn_id
        
