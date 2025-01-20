from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from services.spimex_service import get_last_trading_dates

router = APIRouter(prefix="/spimex")


@router.get("/last-trading-dates")
async def get_last_trading_dates_route(nums_days: int = 5, db: AsyncSession = Depends(get_db)):
    try:
        trading_dates = await get_last_trading_dates(db, nums_days)
        return [date for date in trading_dates]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения данных: {e}")
