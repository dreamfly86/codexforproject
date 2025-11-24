from datetime import date

from sqlalchemy import Column, Date, Float, Integer, String

from backend.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(120), nullable=False)
    size = Column(String(20), nullable=False)
    category = Column(String(80), nullable=False)
    sale_date = Column(Date, nullable=False, default=date.today)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price
