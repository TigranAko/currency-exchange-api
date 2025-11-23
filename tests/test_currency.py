from pathlib import Path

import pytest
from fastapi import HTTPException
from httpx import Response

from app.api.schemas.currency import SCurrency
from app.utils import external_api as eapi


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
def test_make_requests(mocker, res_json):
    status_code = res_json["status_code"]
    mock_get = mocker.patch("httpx.get")
    mock_get.return_value.json = lambda: res_json
    mock_get.return_value.status_code = status_code

    # костыль для использования встроенного raise_for_status
    real_response = Response(status_code, request=mock_get)
    mock_get.return_value.raise_for_status = real_response.raise_for_status

    url = "https://example.com"

    if "detail" in res_json.keys():  # Если есть ошибка
        # Проверить что вызываются нужные ошибки
        with pytest.raises(HTTPException) as exc:
            response = eapi.make_request(url, headers={})
        response = {
            "status_code": exc.value.status_code,
            "json": {"detail": exc.value.detail},
        }
        # assert response["json"]["detail"] == res_json["detail"]

        # Time out
        # connection
        # http
        # request
        # value

    else:  # Если ошибок нет
        response = eapi.make_request(url, headers={})
        assert response["json"]["json"] == res_json["json"]

        assert len(response["json"]) == 2
        assert response["status_code"] == status_code
        assert response["json"] == res_json
    mock_get.assert_called_once()
    # mock_get.return_value.raise_for_status.assert_called_once()


def test_get_currency_exchange(mocker):
    res_json = {
        "date": "2005-01-01",
        "historical": True,
        "info": {"quote": 0.51961, "timestamp": 1104623999},
        "query": {"amount": 10, "from": "USD", "to": "GBP"},
        "result": 5.1961,
        "success": True,
    }
    mock_get = mocker.patch("httpx.get")
    mock_get.return_value.json = lambda: res_json
    mock_get.return_value.status_code = 200
    currency = SCurrency(**{"currency_to": "GBP", "currency_from": "Usd", "amount": 10})

    response = eapi.get_currency_exchenge(currency)
    assert response["status_code"] == 200
    assert response["json"]["result"] == 5.1961
    mock_get.assert_called_once()


def test_get_currencies_from_json():
    currencies = eapi.get_currencies_from_json()
    assert len(currencies) == 172


def test_currency_json(mocker):
    file_name = "test.json"
    file_path = Path(file_name)
    res_json = {
        "currencies": {"AED": "United Arab Emirates Dirham", "AFN": "Afghan Afghani"}
    }
    mock_get = mocker.patch("httpx.get")
    mock_get.return_value.json = lambda: res_json
    mock_get.return_value.status_code = 200

    eapi.get_currency_list(
        file_name=file_name
    )  # тут отправляется запрос и сохраняется в файле
    mock_get.assert_called_once()
    assert file_path.exists()

    currencies_from_file = eapi.get_currencies_from_json(file_name)  # чтение из файла
    assert currencies_from_file == res_json["currencies"]

    file_path.unlink()
    assert not file_path.exists()
