from app.services import ProductsService


def test_product_services():
    product = ProductsService()

    add_product = product.add_products("The Ramayana", "Books", "982 Gm", 90, 750245)
    assert add_product.price == 90 


    add_stock = product.add_stock(72, 1112, 50, "Stock")
    assert add_stock == 1112

    show_product = product.show_products(750245)
    for data in show_product:
        assert data.warehouse_id == 750245

