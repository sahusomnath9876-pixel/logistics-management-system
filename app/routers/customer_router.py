from app.services import CustomerService, PaymentsService, verify_token, verify_role, OrderService
from fastapi import APIRouter, Depends
from app.database import get_db
from app.repositories import UserRepo
from app.schemas import ProductDetails, AddCart, Orders,  OrderDetails, CustomerCart, OrderPlace
from app.schemas import UPIPayment, CARDPayment, CODPayment, UserDetails, CustomerDetails, UpdateCustomer
from typing import Union


router = APIRouter(prefix="/customer", tags=["Customer Service"], dependencies=[Depends(verify_role("Customer"))])



@router.get("/customer/view", status_code=200, response_model=tuple[UserDetails, CustomerDetails])
def get_customer(db=Depends(get_db), current_user = Depends(verify_token)):
    customer = CustomerService(current_user["user_id"], db)

    customer_data = customer.get_customer()
    return customer_data




@router.get("/search", status_code=200, response_model=list[ProductDetails])
def search_products(search_keyword : str, db=Depends(get_db), current_user = Depends(verify_token)):
    customer = CustomerService(current_user["user_id"], db)

    search = customer.search_product(search_keyword)
    return search 


@router.post("/cart/add", status_code=200)
def add_cart(product : AddCart, db=Depends(get_db), current_user = Depends(verify_token)):
    customer = CustomerService(current_user["user_id"], db)

    add = customer.add_to_cart(product.product_id, product.quantity)
    return{
        "message" : "Product Added Successfuly"
    }


@router.get("/cart/show", status_code=200, response_model=list[CustomerCart]) #need to show cart_table id to frontend to perform delete operation
def get_cart(db=Depends(get_db), current_user = Depends(verify_token)):
    customer = CustomerService(current_user["user_id"], db)

    cart_data = customer.show_cart_data()
    return cart_data    


@router.delete("/cart/delete", status_code=200)
def remove_from_cart(cart_id : int, db=Depends(get_db), current_user = Depends(verify_token)):
    customer = CustomerService(current_user["user_id"], db)

    delete = customer.remove_from_cart(cart_id)
    if delete:
        return{
         "message" : "Product Removed From Cart Successfuly"
            }

def order_place(db=Depends(get_db), current_user = Depends(verify_token)):
    order = OrderService(current_user["customer_id"], db)

    new_order = order.place_order()
    return new_order

@router.post("/order/place", status_code=201, response_model=OrderPlace)
def pay_for_order(pay : Union[UPIPayment, CARDPayment, CODPayment], db=Depends(get_db), current_user = Depends(verify_token), current_order = Depends(order_place)):
    payment = PaymentsService(current_user["customer_id"], db)
    if isinstance(pay, UPIPayment):
        paying = payment.make_payment(current_order.order_id, current_order.total_amount, **pay.model_dump())
        if paying:
            return current_order
    elif isinstance(pay, CARDPayment):
        paying = payment.make_payment(current_order.order_id, current_order.total_amount, **pay.model_dump())
        if paying:
            return current_order
    elif isinstance(pay, CODPayment):
        paying = payment.make_payment(current_order.order_id, current_order.total_amount, **pay.model_dump())
        if paying:
            return current_order


@router.get("/order/view", status_code=200, response_model=list[Orders])
def view_my_orders(db=Depends(get_db), current_user = Depends(verify_token)):
    order = OrderService(current_user["customer_id"], db)

    my_orders = order.show_my_orders()
    return my_orders


@router.get("/order/{order_id}", status_code=200, response_model=list[OrderDetails])
def view_order_details(order_id : str, db=Depends(get_db), current_user=Depends(verify_token)):
    order = OrderService(current_user["customer_id"], db)

    order_details = order.show_order_details(order_id)
    return order_details


@router.delete("/order/delete")
def cancelled_my_order(order_id : str, db=Depends(get_db), current_user=Depends(verify_token)):
    order = OrderService(current_user["customer_id"], db)

    cancelled = order.cancel_my_order(order_id)
    if cancelled:
        return{
        "messsage" : f"Order Id {order_id} Cancelled Sucessfuly"
        }


@router.patch("/update/self", status_code=204)
def update_customer(user : UpdateCustomer, db=Depends(get_db), current_user = Depends(verify_token)):
    customer = CustomerService(current_user["user_id"], db)

    update = customer.update_customer_details(current_user["customer_id"], user.column, user.new_data)
    return update
