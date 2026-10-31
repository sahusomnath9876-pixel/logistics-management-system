from app.models import Products, Inventory, Warehouse, Managers
from app.database import SessionLocal
from sqlalchemy import select
from typing import Any


class ProductsRepo:
    def __init__(self):
        self.__db = SessionLocal()
        self.__products = Products

    def get_product(self, product_id : int) -> object | None:
        return self.__db.get(self.__products, product_id)

    def add_product(self, **product : Any) -> object | None:
        try:
            new_product = self.__products(**product)
            self.__db.add(new_product)
            self.__db.commit()
            self.__db.refresh(new_product)
            return new_product

        except Exception:
            self.__db.rollback()
            return None
        

    def update_product(self, product_id : int, column_name : str, updated_data : Any) -> int | None: #need to add multiple update at once option that helps user
        try:
            product_data = self.get_product(product_id)
            if product_data:

                if column_name.lower() == "product_name":
                    product_data.product_name = updated_data
                    self.__db.commit()
                elif column_name.lower() == "category":
                    product_data.category = updated_data
                    self.__db.commit()
                elif column_name.lower() == "weight":
                    product_data.weight = updated_data
                    self.__db.commit()
                elif column_name.lower() == "price":
                    product_data.price = updated_data
                    self.__db.commit()
        except Exception:
            self.__db.rollback()
            return None
        else:
            return product_id

    def delete_product(self, product_id : int) -> int:
        try:
            product_data = self.get_product(product_id)
            if product_data:
                self.__db.delete(product_data)
                self.__db.commit()

        except Exception:
            self.__db.rollback()
            return None
        else:
            return product_id

    def browse_product(self, user_search : str) -> object:
            stmt = select(self.__products).where(self.__products.product_name.ilike(f"%{user_search}%") )
            search_data = self.__db.scalars(stmt).all()
            return search_data

      
            

        


class InventoryRepo:
    def __init__(self):
        self.__db = SessionLocal()
        self.__inventory = Inventory

    def get_inventory(self, id):
        return self.__db.get(self.__inventory, id)

    def fetch_inventory(self, product_id, warehouse_id):
        try:
            stmt = select(self.__inventory).where(self.__inventory.product_id == product_id, self.__inventory.warehouse_id == warehouse_id)
            result = self.__db.scalars(stmt).first()
            if result:
                return result.id
        except Exception:
            return None
        
    def get_stock(self, product_id):
        stmt = select(self.__inventory).where(self.__inventory.product_id == product_id)
        results = self.__db.scalars(stmt).all()
        if results:
            for stock_data in results:
                return stock_data.stock
        else:
            return None

    def stock_data(self, id, product_id):
        try:
            stmt = select(self.__inventory).where(self.__inventory.id == id, self.__inventory.product_id == product_id)
            result = self.__db.scalars(stmt).all()
            if result:
                for data in result:
                    return (data.stock, data.reserved_stock)
        except Exception as e:
            return None


    
    def fetch_warehouse(self, product_id, quantity):
        stmt = select(self.__inventory).where(self.__inventory.product_id == product_id and self.__inventory.stock > quantity)
        result = self.__db.scalars(stmt).all()
        if result:
            return result
        else:
            return None


    
    def add_inventory(self, **new_inv):
        try:
            new_inventory = self.__inventory(**new_inv)

            self.__db.add(new_inventory)
            self.__db.commit()
            self.__db.refresh(new_inventory)
            return new_inventory

        except Exception as e:
            self.__db.rollback()
            return None
        

    def update_stock(self, id, product_id, stock_type, updated_stock):
        try:
            stmt = select(self.__inventory).where(self.__inventory.id == id, self.__inventory.product_id == product_id)
            stock_data = self.__db.scalars(stmt).first()
            
            if stock_data:
                if stock_type.lower() == "stock":
                    stock_data.stock = updated_stock
                    self.__db.commit()
                elif stock_type.lower() == "reserved_stock":
                    stock_data.reserved_stock = updated_stock
                    self.__db.commit()

        except Exception:
            self.__db.rollback()
            return None
        else:
            return stock_data.stock


    #stock deletatuon coming as soon as possible


class WarehouseRepo:
    def __init__(self):
        self.__db = SessionLocal()
        self.__warehouse = Warehouse

    def get_warehouse(self, warehouse_id):
        data = self.__db.get(self.__warehouse, warehouse_id)
        if data:
            return data

    

    def add_warehouse(self, **warehouse_data):
        try:
            new_warehouse = self.__warehouse(**warehouse_data)

            self.__db.add(new_warehouse)
            self.__db.commit()
            self.__db.refresh(new_warehouse)

        except Exception:
            self.__db.rollback()
            return None
        else:
            return warehouse_data

    def change_manager(self, warehouse_id, new_manager_id):
        try:
            warehouse_data = self.get_warehouse(warehouse_id)
            if warehouse_data:
                warehouse_data.manager_id = new_manager_id
                self.__db.commit()
        except Exception:
            self.__db.rollback()
            return None
        else:
            return new_manager_id

class ManagersRepo:
    def __init__(self):
        self.db = SessionLocal()
        self.manager_db = Managers

    def create_manager(self, **manger_details):
        try:
            add_manager = self.manager_db(**manger_details)

            self.db.add(add_manager)
            self.db.commit()
            self.db.refresh(add_manager)

        except Exception:
            self.db.rollback()
            return None
        else:
            return add_manager

    def add_manager(self, manager_id, warehouse_id, user_id):
        new_manager = self.create_manager(
            manager_id= manager_id,
            warehouse_id= warehouse_id,
            user_id= user_id
        )
        if new_manager:
            return new_manager

    def get_manager(self, manager_id):
        try:
            data = self.db.get(self.manager_db, manager_id)
            if data:
                return data
        except Exception:
            return None