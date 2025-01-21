from datetime import date
from typing import List

from sqlalchemy import select, and_, cast, Date
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import TradingResults


async def get_last_trading_dates(db: AsyncSession, num_days: int) -> List[str]:
    result = await db.execute(
        select(TradingResults.date)
        .distinct()
        .order_by(TradingResults.date.desc())
        .limit(num_days)
    )
    return result.scalars().all()


async def get_dynamics(db: AsyncSession,
                       oil_id: str,
                       delivery_type_id: str,
                       delivery_basis_id: str,
                       start_date: date,
                       end_date: date) -> List[TradingResults]:
    query = select(TradingResults).where(
        and_(
            cast(TradingResults.date, Date) >= start_date,
            cast(TradingResults.date, Date) <= end_date
        )
    )
    if oil_id:
        query = query.where(TradingResults.oil_id == oil_id)
    if delivery_type_id:
        query = query.where(TradingResults.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        query = query.where(TradingResults.delivery_basis_id == delivery_basis_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_trading_results(db: AsyncSession, oil_id: str, delivery_type_id: str, delivery_basis_id: str) \
        -> List[TradingResults]:
    query = select(TradingResults).order_by(TradingResults.date.desc())
    query = query.limit(10)
    if oil_id:
        query = query.where(TradingResults.oil_id == oil_id)
    if delivery_type_id:
        query = query.where(TradingResults.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        query = query.where(TradingResults.delivery_basis_id == delivery_basis_id)
    result = await db.execute(query)
    return result.scalars().all()
