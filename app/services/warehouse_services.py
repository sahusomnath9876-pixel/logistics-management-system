from app.repositories import WarehouseRepo, ProductsRepo
from app.repositories import InventoryRepo, OrdersRepo, OItemsRepo, ManagersRepo
from typing import Any
from app.exceptions import InvalidCerdiantials, NotFoundError, UnexpectedErrorAccuerd, logger

class WarehouseServices:
    def __init__(self, manager_id : int, db):
        self.manager_id = manager_id
        self.__manager_db = ManagersRepo(db)
        self.__orders_db = OrdersRepo(db)
        self.__order_items_db = OItemsRepo(db)
        

    def pending_orders(self) -> object:

            manager = self.__manager_db.get_manager(self.manager_id)
            if not manager:
                raise NotFoundError("No Manager Found")
            warehouse_id = manager.warehouse_id
            orders = self.__order_items_db.show_pending_orders(warehouse_id)
            if not orders:
                raise NotFoundError("No Orders Found")
            return orders


    def dispatch_orders(self, id : int, status : str) -> object:
        try:
            status = str(status)
            orders = self.pending_orders()
            if not orders:
                raise NotFoundError("No Orders Found")
            order_id = None
            for data in orders:
                if data.id == id:
                    dispatch = self.__order_items_db.update_current_status(data.id, status)
                    if dispatch:
                        order_id = data.order_id

                    
            update_order_status = self.__orders_db.update_status(order_id, "status", status)
            if update_order_status:
                return update_order_status
        except (TypeError, ValueError):
            logger.exception("Invalid Data Type")
            raise


#need to add more ways to update order items and date and time as well...

