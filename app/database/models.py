from .database import Base
from sqlalchemy import Integer, String, Column, Date, Text


class TradingResults(Base):
    __tablename__ = "spimex_trading_results"

    id = Column(Integer, primary_key=True,autoincrement=True)
    exchange_product_id = Column(String)
    exchange_product_name = Column(Text)
    oil_id = Column(String)
    delivery_basis_id = Column(Text)
    delivery_basis_name = Column(String)
    delivery_type_id = Column(String)
    volume = Column(String)
    total = Column(String)
    count = Column(Integer)
    date = Column(String)
    created_on = Column(Date)
    updated_on = Column(Date)