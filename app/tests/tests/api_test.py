import pytest
import httpx


@pytest.mark.asyncio
async def test_last_trading_dates():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:8000/spimex/last-trading-dates?nums_days=4",
                                    headers={"accept": "application/json"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4
    for date in data:
        assert isinstance(date, str)
        assert len(date) == 10


@pytest.mark.asyncio
async def test_get_dynamics():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://127.0.0.1:8000/spimex/get-dynamics?start_date=2025-01-01&end_date=2025-01-09",
            headers={"accept": "application/json"}
        )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    first_record = data[0]

    assert first_record["id"] == 1153
    assert first_record["exchange_product_id"] == "PCV7PUF020A"
    assert first_record[
               "exchange_product_name"] == "Полиэтилен НМПЭ-2 второй сорт, Уфаоргсинтез (самовывоз автотранспортом)"
    assert first_record["oil_id"] == "PCV7"
    assert first_record["delivery_basis_id"] == "PUF"
    assert first_record["delivery_basis_name"] == "Уфаоргсинтез"
    assert first_record["delivery_type_id"] == "A"
    assert first_record["volume"] == "20"
    assert first_record["total"] == "452840"
    assert first_record["count"] == 1
    assert first_record["date"] == "2025-01-09"
    assert first_record["created_on"] == "2024-05-17"
    assert first_record["updated_on"] == "2025-01-15"


@pytest.mark.asyncio
async def test_get_dynamics_oil_id():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://127.0.0.1:8000/spimex/get-dynamics?start_date=2025-01-01&end_date=2025-01-09&oil_id=PC07",
            headers={"accept": "application/json"}
        )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    first_record = data[0]

    assert first_record["id"] == 1246
    assert first_record["exchange_product_id"] == "PC07PUF020A"
    assert first_record[
               "exchange_product_name"] == "Переходные марки балена 04070 (ТУ 20.16.51-103-05766563-2024), Уфаоргсинтез (самовывоз автотранспортом)"
    assert first_record["oil_id"] == "PC07"
    assert first_record["delivery_basis_id"] == "PUF"
    assert first_record["delivery_basis_name"] == "Уфаоргсинтез"
    assert first_record["delivery_type_id"] == "A"
    assert first_record["volume"] == "20"
    assert first_record["total"] == "2550000"
    assert first_record["count"] == 1
    assert first_record["date"] == "2025-01-09"
    assert first_record["created_on"] == "2024-08-06"
    assert first_record["updated_on"] == "2025-01-15"


@pytest.mark.asyncio
async def test_get_dynamics_delivery_basis_id_first_record():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://127.0.0.1:8000/spimex/get-dynamics?start_date=2025-01-01&end_date=2025-01-09&delivery_basis_id=PUF",
            headers={"accept": "application/json"}
        )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    first_record = data[0]
    assert first_record["id"] == 1153
    assert first_record["exchange_product_id"] == "PCV7PUF020A"
    assert first_record[
               "exchange_product_name"] == "Полиэтилен НМПЭ-2 второй сорт, Уфаоргсинтез (самовывоз автотранспортом)"
    assert first_record["oil_id"] == "PCV7"
    assert first_record["delivery_basis_id"] == "PUF"
    assert first_record["delivery_basis_name"] == "Уфаоргсинтез"
    assert first_record["delivery_type_id"] == "A"
    assert first_record["volume"] == "20"
    assert first_record["total"] == "452840"
    assert first_record["count"] == 1
    assert first_record["date"] == "2025-01-09"
    assert first_record["created_on"] == "2024-05-17"
    assert first_record["updated_on"] == "2025-01-15"


@pytest.mark.asyncio
async def test_get_trading_results_first_record():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://127.0.0.1:8000/spimex/get-trading-results",
            headers={"accept": "application/json"}
        )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    first_record = data[0]
    assert first_record["id"] == 1376
    assert first_record["exchange_product_id"] == "A692NVY060F"
    assert first_record[
               "exchange_product_name"] == "Бензин (АИ-92-К5) (ГОСТ 32513-2013/ГОСТ 32513-2023), ст. Новоярославская (ст. отправления)"
    assert first_record["oil_id"] == "A692"
    assert first_record["delivery_basis_id"] == "NVY"
    assert first_record["delivery_basis_name"] == "ст. Новоярославская"
    assert first_record["delivery_type_id"] == "F"
    assert first_record["volume"] == "1260"
    assert first_record["total"] == "64200060"
    assert first_record["count"] == 16
    assert first_record["date"] == "2025-01-14"
    assert first_record["created_on"] == "2024-11-20"
    assert first_record["updated_on"] == "2025-01-15"


@pytest.mark.asyncio
async def test_get_trading_results_oil_id_A695():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://127.0.0.1:8000/spimex/get-trading-results?oil_id=A695",
            headers={"accept": "application/json"}
        )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    first_record = data[0]
    assert first_record["id"] == 1276
    assert first_record["exchange_product_id"] == "A695ENU025A"
    assert first_record[
               "exchange_product_name"] == "Бензин (АИ-95-К5) (ГОСТ 32513-2013/ГОСТ 32513-2023), Елховский НПЗ (самовывоз автотранспортом)"
    assert first_record["oil_id"] == "A695"
    assert first_record["delivery_basis_id"] == "ENU"
    assert first_record["delivery_basis_name"] == "Елховский НПЗ"
    assert first_record["delivery_type_id"] == "A"
    assert first_record["volume"] == "75"
    assert first_record["total"] == "4200025"
    assert first_record["count"] == 2
    assert first_record["date"] == "2025-01-14"
    assert first_record["created_on"] == "2024-09-23"
    assert first_record["updated_on"] == "2025-01-15"


@pytest.mark.asyncio
async def test_get_trading_results_oil_id_A695_delivery_type_id_A():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://127.0.0.1:8000/spimex/get-trading-results?oil_id=A695&delivery_type_id=A",
            headers={"accept": "application/json"}
        )

    assert response.status_code == 200

    # Преобразуем ответ в JSON
    data = response.json()

    assert len(data) > 0

    first_record = data[0]
    assert first_record["id"] == 1276
    assert first_record["exchange_product_id"] == "A695ENU025A"
    assert first_record[
               "exchange_product_name"] == "Бензин (АИ-95-К5) (ГОСТ 32513-2013/ГОСТ 32513-2023), Елховский НПЗ (самовывоз автотранспортом)"
    assert first_record["oil_id"] == "A695"
    assert first_record["delivery_basis_id"] == "ENU"
    assert first_record["delivery_basis_name"] == "Елховский НПЗ"
    assert first_record["delivery_type_id"] == "A"
    assert first_record["volume"] == "75"
    assert first_record["total"] == "4200025"
    assert first_record["count"] == 2
    assert first_record["date"] == "2025-01-14"
    assert first_record["created_on"] == "2024-09-23"
    assert first_record["updated_on"] == "2025-01-15"


@pytest.mark.asyncio
async def test_get_trading_results_oil_id_A695_delivery_type_id_A_delivery_basis_id_ENU():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://127.0.0.1:8000/spimex/get-trading-results?oil_id=A695&delivery_type_id=A&delivery_basis_id=ENU",
            headers={"accept": "application/json"}
        )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

    first_record = data[0]
    assert first_record["id"] == 1276
    assert first_record["exchange_product_id"] == "A695ENU025A"
    assert first_record[
               "exchange_product_name"] == "Бензин (АИ-95-К5) (ГОСТ 32513-2013/ГОСТ 32513-2023), Елховский НПЗ (самовывоз автотранспортом)"
    assert first_record["oil_id"] == "A695"
    assert first_record["delivery_basis_id"] == "ENU"
    assert first_record["delivery_basis_name"] == "Елховский НПЗ"
    assert first_record["delivery_type_id"] == "A"
    assert first_record["volume"] == "75"
    assert first_record["total"] == "4200025"
    assert first_record["count"] == 2
    assert first_record["date"] == "2025-01-14"
    assert first_record["created_on"] == "2024-09-23"
    assert first_record["updated_on"] == "2025-01-15"