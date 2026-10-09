from sqlalchemy import Integer, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from typing import TYPE_CHECKING
from .base import Base


if TYPE_CHECKING:
    from .users import Users
    from .inventory import Products

class Customers(Base):
    __tablename__ = "customers"

    customer_id : Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False, unique=True)
    city : Mapped[str] = mapped_column(String(50), nullable=False)
    address : Mapped[str] = mapped_column(String(150), nullable=False)

    user : Mapped["Users"] = relationship(back_populates="customer")
    order : Mapped[list["Orders"]] = relationship(back_populates="customer")


class Orders(Base):
    __tablename__ = "orders"

    order_id : Mapped[int] = mapped_column(primary_key=True)
    customer_id : Mapped[int] = mapped_column(ForeignKey("customers.customer_id"), nullable=False)
    order_date : Mapped[datetime.date] = mapped_column(default=func.current_date)
    status : Mapped[str] = mapped_column(String(50), default="Order Placed", nullable=False)
    total_amount : Mapped[int] = mapped_column(nullable=False)

    customer : Mapped["Customers"] = relationship(back_populates="order")
    order_items : Mapped[list["OrderItems"]] = relationship(back_populates="order")


class OrderItems(Base):
    __tablename__ = "order_items"

    id : Mapped[int] = mapped_column(primary_key=True)
    order_id : Mapped[int] = mapped_column(ForeignKey("orders.order_id"), nullable=False)
    product_id : Mapped[int] = mapped_column(ForeignKey("products.product_id"), nullable=False)
    quantity : Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price : Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal : Mapped[int] = mapped_column(Integer, nullable=False)

    order : Mapped["Orders"] = relationship(back_populates="order_items")
    products : Mapped["Products"] = relationship(back_populates="order_items")