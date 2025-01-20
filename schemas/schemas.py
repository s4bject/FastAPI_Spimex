from pydantic import BaseModel
from datetime import date
from typing import Optional


class TradingDate(BaseModel):
    trading_date: date


class TradingResult(BaseModel):
    id: int
    oil_id: int
    delivery_type_id: int
    delivery_basis_id: int
    trading_date: date
    volume: Optional[float] = None
    price: Optional[float] = None

    class Config:
        orm_mode = True
