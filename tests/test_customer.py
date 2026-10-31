from app.services import CustomerService


def test_customer_services():
    customer = CustomerService(130363)

    search_product = customer.search_product("I Phone")
    produt_id = [products.product_id for products in search_product]
    assert produt_id == [1112, 1113]

    add_to_cart = customer.add_to_cart(1112, 1)
    assert add_to_cart == "Product Added Successfuly"

    cart_data = customer.show_cart_data()
    assert cart_data.get("success") is True


