
from sqlalchemy import create_engine, Integer, String, ForeignKey, Date, func
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from .base import Base
from typing import TYPE_CHECKING
import datetime

if TYPE_CHECKING:
    from .customers import Customers
    from .inventory import Warehouse


class Users(Base):
    __tablename__ = "users"


    user_id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(50), nullable=False)
    phone : Mapped[str] = mapped_column(String(20), nullable=False)
    password : Mapped[str] = mapped_column(String(150), nullable=False)
    role : Mapped[str] = mapped_column(String(50), nullable=False)
    is_active : Mapped[bool] = mapped_column(default=True)
    created_date : Mapped[datetime.date] = mapped_column(Date(), default=func.current_date)

    customer : Mapped["Customers"] = relationship(back_populates="user")
    deliver_agent : Mapped["DeliveryAgent"] = relationship(back_populates="user")



class DeliveryAgent(Base):

    __tablename__ = "delivery_agents"

    agent_id : Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.user_id"), unique=True, nullable=False)
    avaivility : Mapped[bool] = mapped_column(default=True, nullable=False)
    warehouse_id : Mapped[int] = mapped_column(ForeignKey("warehouses.warehouse_id"), nullable=False)
    vehicle_no : Mapped[str]  = mapped_column(String(50), nullable=False)  

    user : Mapped["Users"] = relationship(back_populates="delivery_agent")
    warehouses : Mapped["Warehouse"] = relationship(back_populates="delivery_agent")





 