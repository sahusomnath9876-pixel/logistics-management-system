from app.services import ProductsService, WarehouseServices, verify_role, verify_token
from app.database import get_db
from fastapi import APIRouter, Depends
from app.schemas import AddProduct, AddStock, ProductDetails, StockDetails, UpdateProduct, OrderDetails


router = APIRouter(prefix="/warehouse", tags=["Warehouse Services"], dependencies=[Depends(verify_role("Manager"))])


@router.post("/product/add", status_code=201, response_model=tuple[ProductDetails, StockDetails])
def add_new_product(product : AddProduct, db=Depends(get_db), current_manager = Depends(verify_token)):
    products = ProductsService(db)

    new_product = products.add_products(product.product_name, product.category,
                                        product.weight, product.price, 
                                        current_manager["warehouse_id"])
    add_image = products.add_products_images(new_product.product_id, product.image_url)
    return new_product

@router.get("/product/view", status_code=200, response_model=list[StockDetails])
def show_all_products(db=Depends(get_db), current_manager = Depends(verify_token)):
    product = ProductsService(db)

    product_data = product.show_products(current_manager["warehouse_id"])
    return product_data


@router.get("/product/view/{product_id}", status_code=200, response_model=ProductDetails)
def show_product_details(product_id : int, db=Depends(get_db)):
    product = ProductsService(db)

    product_data = product.show_product_info(product_id)
    return product_data


@router.patch("/product/add/stock", status_code=200, response_model=StockDetails)
def add_stock(stock : AddStock, db=Depends(get_db)):
    product = ProductsService(db)

    add_stock = product.add_stock(stock.inv_id, stock.product_id, stock.stock)
    return add_stock

@router.patch("/product/update", status_code=204)
def update_product(details : UpdateProduct, db=Depends(get_db)):
    product = ProductsService(db)

    update = product.update_product_details(details.product_id, details.update_type, details.new_data)

    if update:
        return{
            "message" : f"Product Id {update} Updated Sucessfuly"
        }

@router.get("/orders/pending", status_code=200, response_model=list[OrderDetails])
def show_pending_orders(db=Depends(get_db), current_manager=Depends(verify_token)):
    warehouse = WarehouseServices(current_manager["manager_id"], db)

    pending = warehouse.pending_orders()
    return pending


@router.patch("/orders/status/update", status_code=204)
def update_orders_status(id : int, status : str, db=Depends(get_db), current_manager = Depends(verify_token)):
    warehouse = WarehouseServices(current_manager["manager_id"], db)

    update = warehouse.dispatch_orders(id, status)
    if update:
        return{
            "message" : f"Order Id {update.order_id}, {status} Sucessfuly"
        }

@router.post("/product/add/image")
def add_images(product_id : int, image_url : str, db=Depends(get_db), current_manager = Depends(verify_token)):
    product = ProductsService(db)

    add_image = product.add_products_images(product_id, image_url)