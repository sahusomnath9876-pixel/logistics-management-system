from app.repositories import CustomerRepo, UserRepo, ProductsRepo
from app.repositories import InventoryRepo, CartRepo
from app.exceptions import OutOfStock, ProductNotFound, UnexpectedErrorAccuerd, logger, EmptyCart




class CustomerService:
    def __init__(self, user_id : int, db):
        self.user_id = user_id
        self.__user_db = UserRepo(db)
        self.__customer_db = CustomerRepo(db)
        self.__cart_db = CartRepo(db)
        self.__products_db = ProductsRepo(db)
        self.__inventory_db = InventoryRepo(db)
    
    

    def search_product(self, search : str) -> object | None: #stock checking based result comming in next feature
        try:
            search = str(search)
            search_result = self.__products_db.browse_product(search)

        except TypeError:
            return None
        else:
            if search_result:
                return search_result
            else:
                return None

    def add_to_cart(self, product_id : int, quantity : int) -> int:
        try:
            product_id = int(product_id)
            quantity = int(quantity)

            product_stock = self.__inventory_db.get_stock(product_id)
            if not product_stock:
                raise OutOfStock("Product Is Out Of Stock")
            product = self.__products_db.get_product(product_id)
            product_price = product.price
            total_price = quantity * product_price
            if product_stock > quantity:
                user = self.__user_db.get_user("user_id", self.user_id)
                customer_id = user.customer.customer_id
                add_cart = self.__cart_db.add_cart(customer_id, product_id, quantity, total_price)
                if add_cart:
                    return product_id
                else:
                    return UnexpectedErrorAccuerd("Can't Add Product Right Now..")
            else:
                raise OutOfStock("Product Is Out Of Stock")
        except (TypeError, ValueError):
            logger.exception("Invalid Data Type")
            raise

    def show_cart_data(self) -> object:
        user = self.__user_db.get_user("user_id", self.user_id)
        customer_id = user.customer.customer_id
        cart_data = self.__cart_db.get_cart(customer_id)
        if not cart_data:
            raise EmptyCart("Your Cart Is Empty")
            
        else:
            return cart_data

    def remove_from_cart(self, id : int) -> int:
        cart_data = self.show_cart_data()
        if cart_data.get("success"):
            cart = cart_data.get("data")
            for data in cart:
                if data.id == id:
                    remove = self.__cart_db.remove_cart(id)
                    if remove:
                        return id 
                    else:
                        raise UnexpectedErrorAccuerd("Can't Remove Right Now")
                else:
                    raise ProductNotFound("Product Is Not There")

    


            
        
        
                    





                
            




    










    



    
