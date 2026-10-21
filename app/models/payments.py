from sqlalchemy import create_engine, Integer, String, ForeignKey, Date, Time, func
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from .base import Base
from typing import TYPE_CHECKING
from datetime import time, date, datetime


if TYPE_CHECKING:
    from .customers import Customers, Orders



class Payments(Base):
    __tablename__ = "payments"

    txn_id : Mapped[str] = mapped_column(String(100), primary_key=True)
    customer_id : Mapped[int] = mapped_column(ForeignKey("customers.customer_id"))
    order_id : Mapped[str] = mapped_column(ForeignKey("orders.order_id"))
    txn_date : Mapped[date] = mapped_column(Date, default=date.today())
    txn_time : Mapped[time] = mapped_column(Time, default=lambda: datetime.now().time())
    amount : Mapped[int] = mapped_column(Integer, nullable=False)
    txn_method : Mapped[str] = mapped_column(String(50), nullable=False)

    customer : Mapped["Customers"] = relationship(back_populates="payments")
    orders : Mapped["Orders"] = relationship(back_populates="payments")