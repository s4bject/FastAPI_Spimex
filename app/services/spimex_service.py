from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import TradingResults


async def get_last_trading_dates(db: AsyncSession, num_days: int) -> List[datetime]:
    result = await db.execute(
        select(TradingResults.date)
        .distinct()
        .order_by(TradingResults.date.desc())
        .limit(num_days)
    )
    return result.scalars().all()
