from app.services import CustomerService, OrderService
from app.repositories import ProductsRepo

class CustomerDash:
    def __init__(self, user):
        self.user = user
        self.products = ProductsRepo()


    def user_dash_ui(self):
        while True:
            print(f"Welocome, {self.user.name}")
            print("-" * 50)
            print("Options : ")
            print("-" * 50)
            print("1. Search Products\n2. Your Cart\n3. Your Orders\n4. Exit")

            option = input("\nEnter Your Option Here = ")

            try:
                option = int(option)
                return option
            except TypeError:
                print("Invalid Input Type")
            except ValueError:
                print("Invalid Input Type ")

    def search_bar_ui(self):
        while True:
            search = input("Search = ").strip()
            if not search:
                break
            else:
                return search

    def cart_ui(self, cart_data):
        while True:
            print("Your Cart..")
            print("-" * 50)
            print("Product Name\tPrice\tQuantity")
            for data in cart_data:
                product_id = data.product_id
                product = self.products.get_product(product_id)
                print(f"{product.product_name}\t{data.total_price}\t{data.quantity}")
            option = input("Do You Wants To Place An Order (Yes/No) = ").strip().lower()
            if option == "yes":
                return option
            else:
                break

class PlaceOrder:
    def __init__(self, user):
        self.user = user




    def address_ui(self):
        while True:
            if self.user.customer.address == "Not Added":
                print("Please Add Your Address...")
            option = input("Do You Wants To Change Your Address(Yes/No) = ").lower()

            if option == "Yes":
                address = input("Enter Your New Address = ").strip().title()
                if not address:
                    print("Address Requierd...")
                    continue
                if address == "yes":
                    change = CustomerService            
            
    


        