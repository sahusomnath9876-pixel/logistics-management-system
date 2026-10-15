from sqlalchemy import Integer, String, func, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import TYPE_CHECKING
from .base import Base


if TYPE_CHECKING:
    from .users import Users
    from .inventory import Products, Warehouse
    from .payments import Payments

class Customers(Base):
    __tablename__ = "customers"

    customer_id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False, unique=True)
    city : Mapped[str] = mapped_column(String(50), nullable=False)
    address : Mapped[str] = mapped_column(String(150), default="Not Added")

    user : Mapped["Users"] = relationship(back_populates="customer")
    order : Mapped[list["Orders"]] = relationship(back_populates="customer")
    payments : Mapped[list["Payments"]] = relationship(back_populates="customer")
    carts : Mapped[list["CustomerCart"]] = relationship(back_populates="customer")


class Orders(Base):
    __tablename__ = "orders"

    order_id : Mapped[str] = mapped_column(String(50), primary_key=True)
    customer_id : Mapped[int] = mapped_column(ForeignKey("customers.customer_id"), nullable=False)
    order_date : Mapped[date] = mapped_column(Date, default=date.today())
    status : Mapped[str] = mapped_column(String(50), default="Order Placed", nullable=False)
    total_amount : Mapped[int] = mapped_column(nullable=False)
    
    # estimate_date : Mapped[date] = mapped_column(Date)


    customer : Mapped["Customers"] = relationship(back_populates="order")
    order_items : Mapped[list["OrderItems"]] = relationship(back_populates="order")
    


class OrderItems(Base):
    __tablename__ = "order_items"

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id : Mapped[str] = mapped_column(String(50), ForeignKey("orders.order_id"), nullable=False)
    product_id : Mapped[int] = mapped_column(ForeignKey("products.product_id"), nullable=False)
    quantity : Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price : Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal : Mapped[int] = mapped_column(Integer, nullable=False)
    assigned_warehouse : Mapped[int] = mapped_column(Integer, nullable=True)
    expected_delivery : Mapped[date] = mapped_column(Date, nullable=True)
    current_status : Mapped[str] = mapped_column(String(50), default="Order Placed")

    order : Mapped["Orders"] = relationship(back_populates="order_items")
    products : Mapped["Products"] = relationship(back_populates="order_items")

class CustomerCart(Base):
    __tablename__ = "customer_cart"

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id : Mapped[int] = mapped_column(ForeignKey("customers.customer_id"))
    product_id : Mapped[int] = mapped_column(Integer, nullable=False)
    qunatity : Mapped[int] = mapped_column(Integer, nullable=False)
    total_price : Mapped[int] = mapped_column(Integer, nullable=False)

    customer : Mapped["Customers"] = relationship(back_populates="carts")



    