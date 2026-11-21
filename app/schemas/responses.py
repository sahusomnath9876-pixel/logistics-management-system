from pydantic import BaseModel, ConfigDict
from datetime import date


class UserResponse(BaseModel):
    user_id : int
    mobile_no : str

    model_config = ConfigDict(from_attributes=True)


class SignUpResponse(BaseModel):
    user_id : int

    model_config = ConfigDict(from_attributes=True)

class ProductDetails(BaseModel):
    product_id : int
    product_name : str
    category : str
    price : int

    model_config = ConfigDict(from_attributes=True)


class CustomerCart(BaseModel):
    id : int
    product_id : int
    quantity : int
    total_price : int

    model_config = ConfigDict(from_attributes=True)

class OrderPlace(BaseModel):
    order_id : str
    customer_id : int
    order_date : date
    status : str
    total_amount : int
    payment : str

    model_config = ConfigDict(from_attributes=True)

class OrderDetails(BaseModel):
    id : int
    order_id : str
    product_id : int
    quantity : int
    unit_price : int
    subtotal : int
    expected_delivery : date
    current_status : str

    model_config = ConfigDict(from_attributes=True)


class Orders(BaseModel):
    order_id : str
    customer_id : int
    order_date: date
    status : str
    total_amount : int
    payment : str

    model_config = ConfigDict(from_attributes=True)

class UserDetails(BaseModel):
    name : str
    mobile_no : str


    model_config = ConfigDict(from_attributes=True)

class CustomerDetails(BaseModel):
    city : str
    address : str

    model_config = ConfigDict(from_attributes=True)

class ProductImages(BaseModel):
    product_id : int
    image_url : str

    model_config = ConfigDict(from_attributes=True)

class ProductDetails(BaseModel):
    product_id : int
    product_name : str
    category : str
    weight : str
    price : int
    images : list[ProductImages] = []

    model_config = ConfigDict(from_attributes=True)

class StockDetails(BaseModel):
    id : int
    warehouse_id : int
    product_id : int
    stock : int
    reserved_stock : int

    model_config = ConfigDict(from_attributes=True)

