import os
import sys

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.database import get_db
from app.database.models import TradingResults
from app.main import app


@pytest.fixture
def mock_async_session():
    session = AsyncMock(spec=AsyncSession)
    session.execute.return_value = MagicMock(scalars=MagicMock(return_value=MagicMock(all=MagicMock())))
    return session


@pytest.fixture
def mock_redis():
    with patch("database.redis_client.redis_client") as mock:
        mock.get.return_value = None
        yield mock


@pytest.fixture
def client(mock_async_session):
    app.dependency_overrides[get_db] = lambda: mock_async_session
    return TestClient(app)


@pytest.fixture
def sample_trading_results():
    from datetime import date
    return [
        TradingResults(
            id=1,
            oil_id="A001",
            delivery_type_id="DT01",
            delivery_basis_id="DB01",
            date="2023-10-01",
            created_on=date(2023, 10, 1),
            updated_on=date(2023, 10, 2),
            volume="1000",
            total="50000"
        )
    ]