from app.repositories import WarehouseRepo, ProductsRepo
from app.repositories import InventoryRepo, ManagersRepo


class ProductsService:
    def __init__(self):
        self.products_db = ProductsRepo()
        self.inventory_db = InventoryRepo()
        self.warehouse_db = WarehouseRepo()


    def add_products(self, p_name, category, weight, price, warehouse_id):
        try:            
            product_name = str(p_name)
            category = str(category)
            weight = str(weight)
            price = int(price)
            warehouse_id = int(warehouse_id)

            add_product = self.products_db.add_product(
                product_name= product_name,
                category= category,
                weight= weight,
                price= price,
            )
            if not add_product:
                return{"success" : False, "message" : "Error While Adding Your Product", "data" : None}
            
            add_inv = self.inventory_db.add_inventory(
                warehouse_id= warehouse_id,
                product_id= add_product.product_id,
                stock= 0,
                reserved_stock= 0
            )
            if not add_inv:
                delete_product= self.products_db.delete_product(add_product.product_id)
                return{"success" : False, "message" : "Error While Adding Your Product", "data" : None}
            return{"success" : True, "message" : "Product Added Successfuly", "data" : add_inv.id}
        except TypeError:
            return{"success" : False, "message" : "Invalid Data Type", "data" : None}
        except Exception as e:
            return{"success" : False, "message" : f"Error {e} ", "data" : None}
        
    def add_stock(self, inv_id, product_id, s_type, stock):
            
        try:
            inv_id = int(inv_id)
            inv_db = self.inventory_db.get_inventory(inv_id)
            if not inv_db:
                return{"success" : False, "message" : "Inventory Not Exists", "data" : None}
            product_id = int(product_id)
            if inv_db.product_id != product_id:
                return{"success" : False, "message" : "No Product Founded", "data" : None}            
            s_type = str(s_type)
            stock = int(stock)
            add_stock = self.inventory_db.update_stock(inv_id, product_id, s_type, stock)

            if not add_stock:
                return{"success" : False, "message" : "Error while add stock of your Product", "data" : None}
            else:
                return{"success" : True, "message" : "Stock Added Successfuly", "data" : inv_id}
        except TypeError:
            return{"success" : False, "message" : "Invalid Data Type", "data" : None}
        except Exception as e:
            return{"success" : False, "message" : f"Error {e}", "data" : None}


    def show_products(self, warehouse_id):
        try:
            warehouse_id = int(warehouse_id)
            warehouse = self.warehouse_db.get_warehouse(warehouse_id)
            inventory = warehouse.inventory
            if not inventory:
                return{"success" : False, "message" : "Can't Found Any Inventory", "data" : None}       
            return{"success" : True, "message" : "Inventory Data Founded Successfuly", "data" : inventory}
        except TypeError:
            return{"success" : False, "message" : "Invalid Data Type", "data" : None}
        except Exception as e:
            return{"success" : False, "message" : f"Error {e}", "data" : None}

    def update_product_details(self, product_id, u_type, new_data):
        try:
            product_id = int(product_id)
            products = self.products_db.get_product(product_id)
            if not products:
                return{"success" : False, "message" : "Invalid Product Id", "data" : None}
            u_type = str(u_type).lower()
            if u_type == "price":
                new_data = int(new_data)
            else:
                new_data = str(new_data)
            update_info = self.products_db.update_product(product_id, u_type, new_data)
            if not update_info:
                return{"success" : False, "message" : "Error While Updating Your Product", "data" : None}
            return{"success" : True, "message" : f"Product {products.product_name} Updated Successfuly", "data" : None}
        except TypeError:
            return{"success" : False, "message" : "Invalid Data Type", "data" : None}
        except Exception as e:
            return{"success" : False, "message" : f"Error {e}", "data" : None}

