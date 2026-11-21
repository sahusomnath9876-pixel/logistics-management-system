from fastapi import APIRouter, Depends
from app.services import ProductsService
from app.database import get_db
from app.schemas import ProductDetails, ProductImages


router = APIRouter(prefix=("/products"), tags=["Products"])


@router.get("/all", status_code=200, response_model=list[ProductDetails])
def get_products_data(db=Depends(get_db)):
    product = ProductsService(db)

    product_data = product.get_all_products_data()
    return product_data


@router.get("/images", status_code=200, response_model=list[ProductImages])
def get_product_image(product_id : int, db=Depends(get_db)):
    product = ProductsService(db)

    image_data = product.get_images(product_id)
    return image_data

