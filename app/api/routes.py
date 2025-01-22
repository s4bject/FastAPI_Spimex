from datetime import date, datetime
from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from services.spimex_service import get_last_trading_dates, get_dynamics, get_trading_results

from shcemas.schemas import TradingResultsResponse

from services.cache import cache_response

router = APIRouter(prefix="/spimex")


@router.get("/last-trading-dates")
@cache_response()
async def get_last_trading_dates_route(nums_days: Annotated[int, Field(ge=1)], request: Request,
                                       db: AsyncSession = Depends(get_db)):
    try:
        trading_dates = await get_last_trading_dates(db, nums_days)
        return [date for date in trading_dates]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения данных: {e}")


@router.get("/get-dynamics", response_model=List[TradingResultsResponse])
@cache_response()
async def get_dynamics_route(start_date: str,
                             end_date: str,
                             request: Request,
                             oil_id: Optional[str] = None,
                             delivery_type_id: Optional[str] = None,
                             delivery_basis_id: Optional[str] = None,
                             db: AsyncSession = Depends(get_db)):
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        query = await get_dynamics(db, oil_id, delivery_type_id, delivery_basis_id, start_date_obj, end_date_obj)
        response = [TradingResultsResponse.from_orm(item) for item in query]
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения данных: {e}")


@router.get("/get-trading-results", response_model=List[TradingResultsResponse])
@cache_response()
async def get_trading_results_route(request: Request, oil_id: Optional[str] = None,
                                    delivery_type_id: Optional[str] = None,
                                    delivery_basis_id: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    try:
        query = await get_trading_results(db, oil_id, delivery_type_id, delivery_basis_id)
        response = [TradingResultsResponse.from_orm(item) for item in query]
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения данных: {e}")
