from app.repositories import WarehouseRepo, ProductsRepo
from app.repositories import InventoryRepo, ManagersRepo
from typing import Any
from app.exceptions import InvalidCerdiantials, NotFoundError, UnexpectedErrorAccuerd, logger

class ProductsService:
    def __init__(self, db):
        self.__products_db = ProductsRepo(db)
        self.__inventory_db = InventoryRepo(db)
        self.__warehouse_db = WarehouseRepo(db)


    def add_products(self, p_name : str, category : str, weight : str, price : int, warehouse_id : int) -> object :
        try:            
            product_name = str(p_name)
            category = str(category)
            weight = str(weight)
            price = int(price)
            warehouse_id = int(warehouse_id)

            add_product = self.__products_db.add_product(
                product_name= product_name,
                category= category,
                weight= weight,
                price= price,
            )
            if not add_product:
                raise UnexpectedErrorAccuerd("Error While Adding Your Products")
            
            add_inv = self.__inventory_db.add_inventory(
                warehouse_id= warehouse_id,
                product_id= add_product.product_id,
                stock= 0,
                reserved_stock= 0
            )
            if not add_inv:
                delete_product= self.__products_db.delete_product(add_product.product_id)
                raise UnexpectedErrorAccuerd("Error While Adding Your Products")
            return add_product
        except (TypeError, ValueError):
            logger.exception("Invalid Data Type")
            raise

        
    def add_stock(self, inv_id : int, product_id : int, stock : int, s_type : str = "stock") -> object:
            
        try:
            inv_id = int(inv_id)
            inv_db = self.__inventory_db.get_inventory(inv_id)
            if not inv_db:
                raise NotFoundError("Invantory Not Exists")
            product_id = int(product_id)
            if inv_db.product_id != product_id:
                raise NotFoundError("Product Not Found")          
            s_type = str(s_type)
            stock = int(stock)
            add_stock = self.__inventory_db.update_stock(inv_id, product_id, s_type, stock)

            if not add_stock:
                raise UnexpectedErrorAccuerd("Error While Adding Your Products Stock")
            else:
                return add_stock
        except (TypeError, ValueError):
            logger.exception("Invalid Data Type")
            raise



    def show_products(self, warehouse_id : int) -> object:
        try:
            warehouse_id = int(warehouse_id)
            warehouse = self.__warehouse_db.get_warehouse(warehouse_id)
            inventory = warehouse.inventory
            if not inventory:
                raise NotFoundError("Can't Find These Product Details")      
            return inventory
        except (TypeError, ValueError):
            logger.exception("Invalid Data Type")
            raise


    def update_product_details(self, product_id : int, u_type : str, new_data : Any) -> int:
        try:
            product_id = int(product_id)
            products = self.__products_db.get_product(product_id)
            if not products:
                raise InvalidCerdiantials("Invalid Product Id")
            u_type = str(u_type).lower()
            if u_type == "price":
                new_data = int(new_data)
            else:
                new_data = str(new_data)
            update_info = self.__products_db.update_product(product_id, u_type, new_data)
            if not update_info:
                raise UnexpectedErrorAccuerd("Error While Updating Your Products")
            return product_id
        except (TypeError, ValueError):
            logger.exception("Invalid Data Type")
            raise


