from app.services import WarehouseServices


def test_warehouse_service():
    warehouse = WarehouseServices(14552)

    pending_orders = warehouse.pending_orders()
    for order_data in pending_orders:
        assert order_data.assigned_warehouse == 750245

    dispatch_order = warehouse.dispatch_orders(5, "Dispatched")
    assert dispatch_order.order_id == "OD658290"