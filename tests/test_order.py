from app.services import OrderService



def test_orders():
    order = OrderService(10212)

    place_order = order.place_order()
    assert place_order.customer_id == 10212

    my_orders = order.show_my_orders()
    for order_data in my_orders:
        assert order_data.customer_id == 10212






  



    

