from app.repositories import CartRepo, UserRepo, CustomerRepo, ProductsRepo, OrdersRepo
from app.repositories import OItemsRepo, InventoryRepo, WarehouseRepo, get_travel_data
from app.services import CustomerService
from datetime import datetime, timedelta
import random
from typing import Any

class OrderService:
    def __init__(self, customer_id : int):
        self.customer_id = customer_id
        self.user_db = UserRepo()
        self.customer_db = CustomerRepo()
        self.cart_db = CartRepo()
        self.orders_db = OrdersRepo()
        self.order_items_db = OItemsRepo()
        self.products_db = ProductsRepo()
        self.inventory_db = InventoryRepo()

    def order_id_maker(self) -> int | None:
        random_nums = str(random.randint(100000, 900000))
        alpha = "OD"
        order_id = alpha + random_nums
        return order_id

    def update_stock_data(self, id : int, product_id : int, quantity : int) -> int | None:
        stock, reserved_stock = self.inventory_db.stock_data(id, product_id)
        if stock:
            updated_stock = stock - quantity
            save_stock = self.inventory_db.update_stock(id, product_id, "stock", updated_stock)
            if save_stock:
                return save_stock
            
    def add_stock_data(self, id : int, product_id : int, quantity : int) -> int | None:
        stock, reserved_stock = self.inventory_db.stock_data(id, product_id)
        if stock:
            updated_stock = stock + quantity
            save_stock = self.inventory_db.update_stock(id, product_id, "stock", updated_stock)
            if save_stock:
                return save_stock


    def availabe_warehouse(self, product_id : int, quantity : int) -> tuple:
        verify = self.inventory_db.fetch_warehouse(product_id, quantity)
        customer = self.customer_db.get_customer(self.customer_id)
        user_id = customer.user.user_id
        user = self.user_db.get_user("user_id", user_id)
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


    def create_order(self) -> dict[str, Any]:
        try:
            order_id = self.order_id_maker()
            new_order = self.orders_db.create_order(
                order_id= order_id,
                customer_id= self.customer_id,
                total_amount= 0
            )
            if not new_order:
                return{"success" : False, "message" : "Error While Placing Your Order", "data" : None}
            else:
                return{"success" : True, "message" : "Order Created Successfuly", "data" : new_order}
        except Exception as e:
            return{"success" : False, "message" : f"Error {e}", "data" : None}

    def save_order_details(self) -> dict[str, Any]:
        try:
            created_order = self.create_order()
            if not created_order.get("success"):
                return created_order.get("message")
            order_data = created_order.get("data")
            customer_cart = self.cart_db.get_cart(self.customer_id)
            if not customer_cart:
                return{"success" : False, "message" : "Empty Cart", "data" : None}
            total_amount = 0
            for cart_data in customer_cart:
                total_amount += cart_data.total_price
                products = self.products_db.get_product(cart_data.product_id)
                order_items = self.order_items_db.create_order_items(
                    order_id= order_data.order_id,
                    product_id= cart_data.product_id,
                    quantity= cart_data.qunatity,
                    unit_price= products.price,
                    subtotal= cart_data.total_price
                )
                if not order_items:
                    delete_order = self.orders_db.delete_order(order_data.order_id)
                    if delete_order:
                        return{"success" : False, "message" : "Unable To Place Your Order", "data" : None}
                else:
                    warehouse_id, delivery_time, inventory_id = self.availabe_warehouse(cart_data.product_id, cart_data.qunatity)
                    if not warehouse_id:
                        return{"success" : False, "message" : "Unable to Find a warehouse", "data" : None}
                    delivery_date = self.excpected_delivery_date(delivery_time)
                    update_date = self.order_items_db.update_order_items(order_items.id, delivery_date)
                    assign_warehouse = self.order_items_db.assign_warehouse(order_items.id, warehouse_id)
                    update_stock = self.update_stock_data(inventory_id, cart_data.product_id, cart_data.qunatity)
                
                        
            update_amount = self.orders_db.update_status(order_data.order_id, "amount", total_amount)
            if update_amount:
                return{"success" : True, "message" : f"Order Placed Successfuly, Order Id {order_data.order_id}", "data" : order_items} #adding hours in next time.....
        except Exception as e:
            return{"success" : False, "message" : f"Error{e}", "data" : None}
        
    def place_order(self) -> dict[str, Any]:
        try:
            customer = self.customer_db.get_customer(self.customer_id)
            if customer.address.lower() == "not added":
                return{"success" : False, "message" : "Unable To Place Your Order, Add Your Address", "data" : None}
            order = self.save_order_details()
            if order.get("success"):
                delete_cart = self.cart_db.delete_cart(self.customer_id)
                if delete_cart:
                    return order.get("message")
            else: 
                return order.get("message")

        except Exception as e:
            return{"success" : False, "message" : "Unable To Place Your Order", "data" : None}
            
    def show_my_orders(self) -> dict[str, Any]:
            order_data = self.orders_db.get_customer_order(self.customer_id)
            if order_data:
                return{"success" : True, "message" : "Data Fetched Successfuly", "data" : order_data}  
            else:
                return{"success" : False, "message" : "You haven't Placed any orders yet..", "data" : None}
    
    def cancel_my_order(self, order_id : str) -> dict[str, Any]: ##we will need to modify this to get status in cancelled and dispatched
        order_data = self.orders_db.get_order(order_id)
        if order_data.status.lower() == "order placed":
            cancelled_order = self.orders_db.update_status(order_id, "status", "Cancelled")
            if not cancelled_order:
                return{"success" : False, "message" : "Sorry We Can't Cancelled This Order", "data" : None}
            cancelled_oi  = self.order_items_db.update_status(order_id, "status", "Cancelled")
            if not cancelled_oi:
                return{"success" : False, "message" : "Sorry We Can't Cancelled This Order", "data" : None}
            order_items = self.order_items_db.fetch_order_items(order_id)
            if order_items:
                for data in order_items:
                    inv_id = self.inventory_db.fetch_inventory(data.product_id, data.assigned_warehouse)
                    stock_data = self.add_stock_data(inv_id, data.product_id, data.quantity)
                        
                return{"success" : True, "message" : "Order cancelled Successfuly", "data" : None}
            return{"success" : False, "message" : "Sorry We Can't Cancelled This Order", "data" : None}
        return{"success" : False, "message" : "Sorry We Can't Cancelled This Order", "data" : None}
                  



        
        
        
        