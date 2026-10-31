from app.services import ProductsService


def test_product_services():
    product = ProductsService()

    add_product = product.add_products("Atomic Habits Book", "Books", "966 Gm", 985, 750245)
    assert add_product.get("success") is True #product already exists

    add_product = product.add_products("Samsun Watch", "Watches", "1256 Gm", 2385, 750245)
    assert add_product.get("success") is True 

    add_stock = product.add_stock(11, 1112, 200, "Stock")
    assert add_stock.get("success") is True

    show_product = product.show_products(750245)
    assert show_product.get("success") is True

    update_product = product.update_product_details(1112, "stock", 500)
    assert update_product.get("success") is True