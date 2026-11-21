from app.repositories import CartRepo, UserRepo, CustomerRepo, ProductsRepo, OrdersRepo
from app.repositories import OItemsRepo, InventoryRepo, get_travel_data
from app.exceptions import UnexpectedErrorAccuerd, EmptyCart, NotFoundError
from datetime import datetime, timedelta
import random
from typing import Any

class OrderService:
    def __init__(self, customer_id : int, db):
        self.customer_id = customer_id
        self.__user_db = UserRepo(db)
        self.__customer_db = CustomerRepo(db)
        self.__cart_db = CartRepo(db)
        self.__orders_db = OrdersRepo(db)
        self.__order_items_db = OItemsRepo(db)
        self.__products_db = ProductsRepo(db)
        self.__inventory_db = InventoryRepo(db)

    def __order_id_maker(self) -> int | None:
        random_nums = str(random.randint(100000, 900000))
        alpha = "OD"
        order_id = alpha + random_nums
        return order_id

    def __update_stock_data(self, id : int, product_id : int, quantity : int) -> int | None:
        stock, reserved_stock = self.__inventory_db.stock_data(id, product_id)
        if stock:
            updated_stock = stock - quantity
            save_stock = self.__inventory_db.update_stock(id, product_id, "stock", updated_stock)
            if save_stock:
                return save_stock
            
    def __add_stock_data(self, id : int, product_id : int, quantity : int) -> int | None:
        stock, reserved_stock = self.__inventory_db.stock_data(id, product_id)
        if stock:
            updated_stock = stock + quantity
            save_stock = self.__inventory_db.update_stock(id, product_id, "stock", updated_stock)
            if save_stock:
                return save_stock


    def __availabe_warehouse(self, product_id : int, quantity : int) -> tuple:
        verify = self.__inventory_db.fetch_warehouse(product_id, quantity)
        customer = self.__customer_db.get_customer(self.customer_id)
        user_id = customer.user.user_id
        user = self.__user_db.get_user("user_id", user_id)
        customer_city = user.customer.city
        if verify:
            distance_diff = float('inf') 
            warehouse_id = None
            delivery_time = None
            for data in verify:
                warehouse_location = data.warehouses.location
                calculate = get_travel_data(warehouse_location, customer_city)
                distance = calculate.get("distance_km")
                time = round(calculate.get("duration_mins") / 60,2) #in hours
                if distance < distance_diff:
                    distance_diff = distance
                    warehouse_id = data.warehouse_id
                    delivery_time = time   
                    inventory_id = data.id
            return warehouse_id, delivery_time, inventory_id
        return None

    def excpected_delivery_date(self, distance_hours : float) -> Any:
        travel_hours = distance_hours
        handling_time = 4
        delivery_buffer = 24

        total_hours = travel_hours + handling_time

        start = datetime.now()
        earliest = start + timedelta(hours=total_hours)
        latest = earliest + timedelta(hours=delivery_buffer)

        expected_date = latest.date()
        return expected_date


    def create_order(self) -> object:
        order_id = self.__order_id_maker()
        new_order = self.__orders_db.create_order(
            order_id= order_id,
            customer_id= self.customer_id,
            total_amount= 0
        )
        if not new_order:
            raise UnexpectedErrorAccuerd("Error While Placing Your Order")
        else:
            return new_order


    def __save_order_details(self) -> object:

            created_order = self.create_order()
            if not created_order:
                raise UnexpectedErrorAccuerd("Error While Creating Your Order")
            order_data = created_order
            customer_cart = self.__cart_db.get_cart(self.customer_id)
            if not customer_cart:
                raise EmptyCart("Your Cart Is Empty")
            total_amount = 0
            for cart_data in customer_cart:
                total_amount += cart_data.total_price
                products = self.__products_db.get_product(cart_data.product_id)
                order_items = self.__order_items_db.create_order_items(
                    order_id= order_data.order_id,
                    product_id= cart_data.product_id,
                    quantity= cart_data.quantity,
                    unit_price= products.price,
                    subtotal= cart_data.total_price
                )
                if not order_items:
                    delete_order = self.__orders_db.delete_order(order_data.order_id)
                    if delete_order:
                        raise UnexpectedErrorAccuerd("Unable To Place Your Order Right Now")
                else:
                    warehouse_id, delivery_time, inventory_id = self.__availabe_warehouse(cart_data.product_id, cart_data.quantity)
                    if not warehouse_id:
                        raise NotFoundError("Unable To Find Warehouse Id")
                    delivery_date = self.excpected_delivery_date(delivery_time)
                    update_date = self.__order_items_db.update_order_items(order_items.id, delivery_date)
                    assign_warehouse = self.__order_items_db.assign_warehouse(order_items.id, warehouse_id)
                    update_stock = self.__update_stock_data(inventory_id, cart_data.product_id, cart_data.quantity)

            update_amount = self.__orders_db.update_status(order_data.order_id, "amount", total_amount)
            if update_amount:
                return update_amount #adding hours in next time.....
        
        
    def place_order(self) -> object:

            customer = self.__customer_db.get_customer(self.customer_id)
            if customer.address.lower() == "not added":
                raise NotFoundError("Your Address Is Not Added Yet")
            order = self.__save_order_details()
            if order:
                delete_cart = self.__cart_db.delete_cart(self.customer_id)
                if delete_cart:
                    return order
            else: 
                return order

            
    def show_my_orders(self) -> object:
            order_data = self.__orders_db.get_customer_order(self.customer_id)
            if order_data:
                return order_data
            else:
                return NotFoundError("Order Not founded")


    def show_order_details(self, order_id : str) -> object:
        order_data = self.__order_items_db.get_order_details(order_id)
        if not order_data:
            raise NotFoundError("Orders Not Founded")
        return order_data
    
    def cancel_my_order(self, order_id : str) -> str: ##we will need to modify this to get status in cancelled and dispatched
        order_data = self.__orders_db.get_order(order_id)
        if order_data.status.lower() == "order placed":
            cancelled_order = self.__orders_db.update_status(order_id, "status", "Cancelled")
            if not cancelled_order:
                raise UnexpectedErrorAccuerd("Unable To Cancel Your Order Right Now")
            cancelled_oi  = self.__order_items_db.update_status(order_id, "status", "Cancelled")
            if not cancelled_oi:
                raise UnexpectedErrorAccuerd("Unable To Cancel Your Order Right Now")
            order_items = self.__order_items_db.fetch_order_items(order_id)
            if order_items:
                for data in order_items:
                    inv_id = self.__inventory_db.fetch_inventory(data.product_id, data.assigned_warehouse)
                    stock_data = self.__add_stock_data(inv_id, data.product_id, data.quantity)
                        
                return order_id
            raise UnexpectedErrorAccuerd("Unable To Cancel Your Order Right Now")
        raise UnexpectedErrorAccuerd("Unable To Cancel Your Order Right Now")
                  



        
        
        
        