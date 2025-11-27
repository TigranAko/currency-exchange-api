from pathlib import Path

import pytest
from fastapi import HTTPException
from httpx import Response

from app.api.schemas.currency import SCurrency
from app.dependencies.external_api import get_currencies_from_json

# from app.utils import external_api as eapi
# from app.services.external_api_service import


@pytest.mark.parametrize(
    "res_json",
    (
        ({"status_code": 200, "json": {"test": "test"}}),
        ({"status_code": 422, "detail": "Таймаут при обращении к внешнему API"}),
        ({"status_code": 422, "detail": "Внешний сервис недоступен"}),
        ({"status_code": 422, "detail": "text"}),
        ({"status_code": 422, "detail": "text"}),
        ({"status_code": 422, "detail": "Некорректный JSON в ответе от API"}),
    ),
)
@pytest.mark.asyncio
async def test_make_requests(api_service, mocker, res_json):
    status_code = res_json["status_code"]
    mock_get = mocker.patch("httpx.AsyncClient.get")
    mock_get.return_value.json = lambda: res_json
    mock_get.return_value.status_code = status_code

    # костыль для использования встроенного raise_for_status
    real_response = Response(status_code, request=mock_get)
    mock_get.return_value.raise_for_status = real_response.raise_for_status

    url = "https://example.com"

    if "detail" in res_json.keys():  # Если есть ошибка
        # Проверить что вызываются нужные ошибки
        with pytest.raises(HTTPException) as exc:
            response = await api_service.make_request(url)
        response = {"detail": exc.value.detail}
        # assert response["json"]["detail"] == res_json["detail"]

        # Time out
        # connection
        # http
        # request
        # value

    else:  # Если ошибок нет
        response = await api_service.make_request(url)
        assert response["json"] == res_json["json"]

        assert len(response) == 2
        assert response == res_json
    mock_get.assert_called_once()
    # mock_get.return_value.raise_for_status.assert_called_once()


@pytest.mark.asyncio
async def test_get_currency_exchange(api_service, mocker):
    res_json = {
        "date": "2005-01-01",
        "historical": True,
        "info": {"quote": 0.51961, "timestamp": 1104623999},
        "query": {"amount": 10, "from": "USD", "to": "GBP"},
        "result": 5.1961,
        "success": True,
    }
    mock_get = mocker.patch("httpx.AsyncClient.get")
    mock_get.return_value.json = lambda: res_json
    currency = SCurrency(**{"currency_to": "GBP", "currency_from": "Usd", "amount": 10})

    response = await api_service.get_currency_exchenge(currency)
    assert response["result"] == 5.1961
    mock_get.assert_called_once()


def test_get_currencies_from_json():
    currencies = get_currencies_from_json()
    assert len(currencies) == 172


@pytest.mark.asyncio
async def test_currency_json(api_service, mocker):
    file_name = "test.json"
    file_path = Path(file_name)
    res_json = {
        "currencies": {"AED": "United Arab Emirates Dirham", "AFN": "Afghan Afghani"}
    }
    mock_get = mocker.patch("httpx.AsyncClient.get")
    mock_get.return_value.json = lambda: res_json

    await api_service.get_currency_list(
        file_name=file_name
    )  # тут отправляется запрос и сохраняется в файле
    mock_get.assert_called_once()
    assert file_path.exists()

    currencies_from_file = get_currencies_from_json(file_name)  # чтение из файла
    assert currencies_from_file == res_json["currencies"]

    file_path.unlink()
    assert not file_path.exists()
