from pydantic import BaseModel
from datetime import date
from typing import Any


class Auth(BaseModel):
    username : str
    password : str

class CustomerSignUp(BaseModel):
    name : str
    mobile_no : str
    password : str
    city : str

class ManagerSignUp(BaseModel):
    name : str
    mobile_no : str
    password : str
    warehouse_id : int
    manager_id : int

class AddCart(BaseModel):
    product_id : int
    quantity : int

class CODPayment(BaseModel):
    method : str = "COD"



class UPIPayment(BaseModel):
    method : str = "UPI"
    upi_id : str

class CARDPayment(BaseModel):
    method : str = "CARD"
    card_number : int
    expiry_date : date
    cvv : int

class AddProduct(BaseModel):
    product_name : str
    category : str
    weight : str
    price : int
    image_url : str

class AddStock(BaseModel):
    inv_id : int
    product_id : int
    stock : int

class UpdateProduct(BaseModel):
    product_id : int
    update_type : str
    new_data : Any

class UpdateCustomer(BaseModel):
    column : str
    new_data : Any