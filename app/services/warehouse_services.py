from app.repositories import WarehouseRepo, ProductsRepo
from app.repositories import InventoryRepo, OrdersRepo, OItemsRepo, ManagersRepo
from typing import Any

class WarehouseServices:
    def __init__(self, manager_id : int):
        self.manager_id = manager_id
        self.__manager_db = ManagersRepo()
        self.__orders_db = OrdersRepo()
        self.__order_items_db = OItemsRepo()
        

    def pending_orders(self) -> dict[str, Any]:
        try:
            manager = self.__manager_db.get_manager(self.manager_id)
            if not manager:
                return{"success" : False, "message" : "No manager found", "data" : None}
            warehouse_id = manager.warehouse_id
            orders = self.__order_items_db.show_pending_orders(warehouse_id)
            if not orders:
                return{"success" : False, "message" : "No Orders Found", "data" : None}
            return{"success" : True, "message" : "Orders Found", "data" : orders}
        except Exception as e:
            return{"success" : False, "message" : f"Error{e}", "data" : None}

    def dispatch_orders(self, id : int, status : str) -> dict[str, Any]:
        try:
            status = str(status)
            orders = self.pending_orders()
            if not orders.get("success"):
                return{"success" : False, "message" : "No Orders Found", "data" : None}
            order_id = None
            for data in orders.get("data"):
                if data.id == id:
                    dispatch = self.__order_items_db.update_current_status(data.id, status)
                    if dispatch:
                        order_id = data.order_id

                    
            update_order_status = self.__orders_db.update_status(order_id, "status", status)
            if update_order_status:
                return{"success" : True, "message" : "Order Proccessed Successfuly", "data" : id}
        except TypeError:
            return{"success" : False, "message" : "Invalid Status Type", "data" : None}
        except Exception:
            return{"success" : False, "message" : "Request Failed", "data" : None}




