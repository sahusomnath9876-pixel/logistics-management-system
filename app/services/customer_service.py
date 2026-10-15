from app.repositories import CustomerRepo, UserRepo, WarehouseRepo, ProductsRepo
from app.repositories import InventoryRepo, OrdersRepo, OItemsRepo, CartRepo, get_travel_data
import random




class CustomerService:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_db = UserRepo()
        self.customer_db = CustomerRepo()
        self.cart_db = CartRepo()
        self.products_db = ProductsRepo()
        self.inventory_db = InventoryRepo()
    
    

    def search_product(self, search): #stock checking based result comming in next feature
        try:
            search = str(search)
            search_result = self.products_db.browse_product(search)

        except TypeError:
            return None
        else:
            if search_result:
                return search_result
            else:
                return None

    def add_to_cart(self, product_id, quantity):
        try:
            product_id = int(product_id)
            quantity = int(quantity)

            product_stock = self.inventory_db.get_stock(product_id)
            if not product_stock:
                return "Product Is Out Of Stock"
            product = self.products_db.get_product(product_id)
            product_price = product.price
            total_price = quantity * product_price
            if product_stock > quantity:
                user = self.user_db.get_user("user_id", self.user_id)
                customer_id = user.customer.customer_id
                add_cart = self.cart_db.add_cart(customer_id, product_id, quantity, total_price)
                if add_cart:
                    return "Product Added Successfuly"
                else:
                    return "Error Accured"
            else:
                return "Product Is Out Of Stock"
        except TypeError:
            return "Invalid Data Type"
        except Exception:
            return "Error"

    def show_cart_data(self):
        user = self.user_db.get_user("user_id", self.user_id)
        customer_id = user.customer.customer_id
        cart_data = self.cart_db.get_cart(customer_id)
        if not cart_data:
            return{"success" : False, "message" : "Empty Cart", "data" : None}
        else:
            return{"success" : True, "message" : "Cart Data Fetched Successfuly", "data" : cart_data}

    def remove_from_cart(self, id):
        cart_data = self.show_cart_data()
        if cart_data.get("success"):
            cart = cart_data.get("data")
            for data in cart:
                if data.id == id:
                    remove = self.cart_db.remove_cart(id)
                    if remove:
                        return{"success" : True, "message" : "Removed Successfuly", "data" : None}
                    else:
                        return{"success" : False, "message" : "Failed", "data" : None}
                else:
                    return{"success" : False, "message" : "Product is not there", "data" : None}


            

            
        
        
                    





                
            




    










    



    
