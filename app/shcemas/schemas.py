from typing import Dict, Any

from pydantic import BaseModel
from datetime import date, datetime


class TradingResultsResponse(BaseModel):
    id: int
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: str
    total: str
    count: int
    date: str
    created_on: date
    updated_on: date

    class Config:
        orm_mode = True
        from_attributes = True
