from app.services import OrderService



def test_orders():
    order = OrderService(10212)

    place_order = order.place_order()
    assert place_order.get("success") is True

    my_orders = order.show_my_orders()
    assert my_orders.get("success") == True







  



    

