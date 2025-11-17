
from app.utils import external_api as eapi
from fastapi import HTTPException
from requests import Response


import pytest


@pytest.mark.parametrize("res_json", (
    ({"status_code": 200, "json": {"test": "test"}}),
    ({"status_code": 422, "detail": "Таймаут при обращении к внешнему API"}),
    ({"status_code": 422, "detail": "Внешний сервис недоступен"}),
    ({"status_code": 422, "detail": "text"}),
    ({"status_code": 422, "detail": "text"}),
    ({"status_code": 422, "detail": "Некорректный JSON в ответе от API"}),
    ))
def test_make_requests(mocker, res_json):
    status_code = res_json["status_code"]
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.json = (lambda: res_json)
    mock_get.return_value.status_code = status_code

    real_response = Response()
    real_response.status_code = status_code
    mock_get.return_value.raise_for_status = real_response.raise_for_status

    url = "https://example.com"

    if "detail" in res_json.keys(): # Если есть ошибка
        # Проверить что вызываются нужные ошибки
        with pytest.raises(HTTPException) as exc:
            response = eapi.make_request(url, headers={})
        response = {
                "status_code": exc.value.status_code,
                "json": {
                "detail": exc.value.detail
                }}
        # assert response["json"]["detail"] == res_json["detail"]

        # Time out
        # connection
        # http
        # request
        # value

    else: # Если ошибок нет
        response = eapi.make_request(url, headers={})
        assert response["json"]["json"] == res_json["json"]


        assert len(response["json"]) == 2
        assert response["status_code"] == status_code
        assert response["json"] == res_json
    mock_get.assert_called_once()
    # mock_get.return_value.raise_for_status.assert_called_once()

