import os
import sys

import pytest
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.services.spimex_service import get_last_trading_dates, get_dynamics, get_trading_results


@pytest.mark.asyncio
async def test_get_last_trading_dates(mock_async_session):
    mock_async_session.execute.return_value.scalars.return_value.all.return_value = ["2023-10-02", "2023-10-01"]

    result = await get_last_trading_dates(mock_async_session, 2)
    assert result == ["2023-10-02", "2023-10-01"]


@pytest.mark.asyncio
async def test_get_dynamics(mock_async_session, sample_trading_results):
    mock_async_session.execute.return_value.scalars.return_value.all.return_value = sample_trading_results

    result = await get_dynamics(
        mock_async_session,
        oil_id="A001",
        delivery_type_id="DT01",
        delivery_basis_id="DB01",
        start_date=date(2023, 10, 1),
        end_date=date(2023, 10, 2)
    )

    assert len(result) == 1
    assert result[0].oil_id == "A001"


@pytest.mark.asyncio
async def test_get_trading_results(mock_async_session, sample_trading_results):
    mock_async_session.execute.return_value.scalars.return_value.all.return_value = sample_trading_results

    result = await get_trading_results(
        mock_async_session,
        oil_id="A001",
        delivery_type_id="DT01",
        delivery_basis_id="DB01"
    )

    assert result[0].volume == "1000"

@pytest.mark.asyncio
async def test_get_last_trading_dates_no_results(mock_async_session):
    mock_async_session.execute.return_value.scalars.return_value.all.return_value = []

    result = await get_last_trading_dates(mock_async_session, 2)
    assert result == []


@pytest.mark.asyncio
async def test_get_last_trading_dates_limit(mock_async_session):
    mock_async_session.execute.return_value.scalars.return_value.all.return_value = ["2023-10-02"]

    result = await get_last_trading_dates(mock_async_session, 5)
    assert result == ["2023-10-02"]


@pytest.mark.asyncio
async def test_get_dynamics_empty(mock_async_session):
    mock_async_session.execute.return_value.scalars.return_value.all.return_value = []

    result = await get_dynamics(
        mock_async_session,
        oil_id="A001",
        delivery_type_id="DT01",
        delivery_basis_id="DB01",
        start_date=date(2023, 9, 1),
        end_date=date(2023, 9, 2)
    )

    assert result == []


@pytest.mark.asyncio
async def test_get_dynamics_partial_params(mock_async_session, sample_trading_results):
    mock_async_session.execute.return_value.scalars.return_value.all.return_value = sample_trading_results

    result = await get_dynamics(
        mock_async_session,
        oil_id=None,
        delivery_type_id="DT01",
        delivery_basis_id=None,
        start_date=date(2023, 10, 1),
        end_date=date(2023, 10, 2)
    )

    assert len(result) == 1
    assert result[0].oil_id == "A001"


@pytest.mark.asyncio
async def test_get_trading_results_empty(mock_async_session):
    mock_async_session.execute.return_value.scalars.return_value.all.return_value = []

    result = await get_trading_results(
        mock_async_session,
        oil_id="B002",
        delivery_type_id="DT02",
        delivery_basis_id="DB02"
    )

    assert result == []


@pytest.mark.asyncio
async def test_get_trading_results_partial_params(mock_async_session, sample_trading_results):
    mock_async_session.execute.return_value.scalars.return_value.all.return_value = sample_trading_results

    result = await get_trading_results(
        mock_async_session,
        oil_id=None,
        delivery_type_id="DT01",
        delivery_basis_id=None
    )

    assert len(result) == len(sample_trading_results)
    assert result[0].oil_id == "A001"


@pytest.mark.asyncio
async def test_get_trading_results_limit(mock_async_session, sample_trading_results):
    mock_async_session.execute.return_value.scalars.return_value.all.return_value = sample_trading_results[:10]

    result = await get_trading_results(
        mock_async_session,
        oil_id="A001",
        delivery_type_id="DT01",
        delivery_basis_id="DB01"
    )

    assert len(result) <= 10
    assert result[0].oil_id == "A001"
