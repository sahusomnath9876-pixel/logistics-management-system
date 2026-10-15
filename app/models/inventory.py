from sqlalchemy import Integer, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .customers import OrderItems, Orders
    from .users import DeliveryAgent, Users


class Products(Base): #product schema needs to redifined.....
    __tablename__ = "products"

    product_id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_name : Mapped[str] = mapped_column(String(50), nullable=False)
    category : Mapped[str] = mapped_column(String(50), nullable=False)
    weight : Mapped[str] = mapped_column(String(50), default="Not Listed")
    price : Mapped[int] = mapped_column(Integer, nullable=False)

    inventory : Mapped[list["Inventory"]] = relationship(back_populates="product")
    order_items : Mapped[list["OrderItems"]] = relationship(back_populates="products")

class Inventory(Base):
    __tablename__ = "inventory"

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    warehouse_id : Mapped[int] = mapped_column(ForeignKey("warehouses.warehouse_id"))
    product_id : Mapped[int] = mapped_column(ForeignKey("products.product_id"), nullable=False)
    stock : Mapped[int] = mapped_column(Integer, nullable=False)
    reserved_stock : Mapped[int] = mapped_column(Integer, nullable=False)

    product : Mapped[list["Products"]] = relationship(back_populates="inventory")
    warehouses : Mapped["Warehouse"] = relationship(back_populates="inventory")



class Warehouse(Base):
    __tablename__ = "warehouses"

    warehouse_id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    warehouse_name : Mapped[str] = mapped_column(String(50), nullable=False)
    manager_id : Mapped[int] = mapped_column()
    location : Mapped[str] = mapped_column(String(50), nullable=False)

    inventory : Mapped[list["Inventory"]] = relationship(back_populates="warehouses")
    delivery_agent : Mapped[list["DeliveryAgent"]] = relationship(back_populates="warehouses")
    manager : Mapped["Managers"] = relationship(back_populates="warehouse")

class Managers(Base):
    __tablename__ = "managers"

    manager_id : Mapped[int] = mapped_column(primary_key=True)
    warehouse_id : Mapped[int] = mapped_column(ForeignKey("warehouses.warehouse_id"), unique=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.user_id"), unique=True)

    warehouse : Mapped["Warehouse"] = relationship(back_populates="manager")
    user : Mapped["Users"] = relationship(back_populates="manager")

    