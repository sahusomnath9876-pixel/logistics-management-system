from app.services import WarehouseServices


def test_warehouse_service():
    warehouse = WarehouseServices(14552)

    pending_orders = warehouse.pending_orders()
    assert pending_orders.get("success") is True

    dispatch_order = warehouse.dispatch_orders(3, "Packed")
    assert dispatch_order.get("success") is True