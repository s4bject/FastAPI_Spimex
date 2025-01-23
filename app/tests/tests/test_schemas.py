import os
import sys

import pytest
from datetime import date, datetime
from pydantic import ValidationError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.shcemas.schemas import TradingResultsResponse


def test_trading_results_response_valid():
    # Case: Valid data
    valid_data = {
        "id": 1,
        "exchange_product_id": "EP01",
        "exchange_product_name": "Oil Product",
        "oil_id": "A001",
        "delivery_basis_id": "DB01",
        "delivery_basis_name": "Basis Name",
        "delivery_type_id": "DT01",
        "volume": "1000",
        "total": "5000",
        "count": 10,
        "date": "2023-10-01",
        "created_on": date(2023, 10, 1),
        "updated_on": date(2023, 10, 2),
    }

    response = TradingResultsResponse(**valid_data)

    assert response.id == 1
    assert response.exchange_product_id == "EP01"
    assert response.volume == "1000"
    assert response.date == "2023-10-01"
    assert response.created_on == date(2023, 10, 1)
    assert response.updated_on == date(2023, 10, 2)


def test_trading_results_response_missing_field():
    incomplete_data = {
        "id": 1,
        "exchange_product_id": "EP01",
        "exchange_product_name": "Oil Product",
        "oil_id": "A001",
        "delivery_basis_id": "DB01",
        "delivery_basis_name": "Basis Name",
        "delivery_type_id": "DT01",
        "volume": "1000",
        "total": "5000",
        "count": 10,
        "created_on": date(2023, 10, 1),
        "updated_on": date(2023, 10, 2),
    }

    with pytest.raises(ValidationError) as exc_info:
        TradingResultsResponse(**incomplete_data)

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("date",)
    assert errors[0]["msg"] == "Field required"


def test_trading_results_response_invalid_field_type():
    invalid_type_data = {
        "id": 1,
        "exchange_product_id": "EP01",
        "exchange_product_name": "Oil Product",
        "oil_id": "A001",
        "delivery_basis_id": "DB01",
        "delivery_basis_name": "Basis Name",
        "delivery_type_id": "DT01",
        "volume": "1000",
        "total": "5000",
        "count": "not-a-number",  # Ошибка здесь
        "date": date(2023, 10, 1),
        "created_on": date(2023, 10, 1),
        "updated_on": date(2023, 10, 2),
    }

    with pytest.raises(ValidationError) as exc_info:
        TradingResultsResponse(**invalid_type_data)

    errors = exc_info.value.errors()
    assert len(errors) == 2
    assert errors[0]["loc"] == ("count",)
    assert errors[0]["msg"].startswith("Input should be a valid integer")


def test_trading_results_response_extra_fields():
    # Case: Extra fields in the input data
    extra_fields_data = {
        "id": 1,
        "exchange_product_id": "EP01",
        "exchange_product_name": "Oil Product",
        "oil_id": "A001",
        "delivery_basis_id": "DB01",
        "delivery_basis_name": "Basis Name",
        "delivery_type_id": "DT01",
        "volume": "1000",
        "total": "5000",
        "count": 10,
        "date": "2023-10-01",
        "created_on": date(2023, 10, 1),
        "updated_on": date(2023, 10, 2),
        "unexpected_field": "unexpected",
    }

    response = TradingResultsResponse(**extra_fields_data)

    assert response.id == 1
    assert not hasattr(response, "unexpected_field")


def test_trading_results_response_with_datetime():
    datetime_data = {
        "id": 1,
        "exchange_product_id": "EP01",
        "exchange_product_name": "Oil Product",
        "oil_id": "A001",
        "delivery_basis_id": "DB01",
        "delivery_basis_name": "Basis Name",
        "delivery_type_id": "DT01",
        "volume": "1000",
        "total": "5000",
        "count": 10,
        "date": "2023-10-01",
        "created_on": datetime(2023, 10, 1, 12, 0).date(),
        "updated_on": datetime(2023, 10, 2, 12, 0).date(),
    }

    response = TradingResultsResponse(**datetime_data)

    assert response.created_on == date(2023, 10, 1)
    assert response.updated_on == date(2023, 10, 2)
