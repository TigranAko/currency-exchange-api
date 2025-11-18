import requests
from fastapi import HTTPException

from app.core.config import ConfigCurrencyExchange

from app.api.schemas.currency import SCurrency
from typing import Any
import json

config = ConfigCurrencyExchange()

headers = {
  "apikey": config.CURRENCY_EXCHANGE_API_KEY.get_secret_value()
}


def make_request(url: str, timeout: float = 60, headers: dict = headers) -> dict[str, int|dict]:
    try:
        response = requests.get(url, timeout=timeout, headers=headers)
        # Нужно заменить raise_for_status на свою обработку ошибок, для более точной информации об ошибках
        response.raise_for_status()  # Проверяет HTTP ошибки (4xx, 5xx)
        return {
                "status_code": response.status_code,
                "json": response.json()
                }

    except requests.exceptions.HTTPError as e:
        # Ошибки HTTP (4xx, 5xx) - уже обработаны raise_for_status()
        raise HTTPException(
            status_code=422,
            detail=f"Ошибка внешнего API: {e.response.status_code}"
        )
    except requests.exceptions.RequestException as e:
        # Все остальные ошибки (таймауты, сетевые проблемы и т.д.)
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка соединения: {str(e)}"
        )
    except ValueError as e:  # Если response.json() не сработает
        raise HTTPException(
            status_code=500,
            detail="Некорректный JSON в ответе от API"
        )



def get_currency_exchenge(currency: SCurrency) -> dict[str, Any]:
    url = f"https://api.apilayer.com/currency_data/convert?to={currency.currency_to}&from={currency.currency_from}&amount={currency.amount}"
    #redis cash
    return make_request(url)



def get_currency_list(file_name = "currency_list.json") -> dict[str, Any]:
    url = "https://api.apilayer.com/currency_data/list"
    response_data = make_request(url)

    curencies = response_data["json"]["currencies"]
    update_currencies_json(curencies, file_name=file_name)

    return response_data


def update_currencies_json(response_json, file_name = "currency_list.json") -> None:
    with open(file_name, 'w', encoding="utf-8") as file:
        json.dump(response_json, file, ensure_ascii=False, indent=4)



def get_currencies_from_json(file_name = "currency_list.json") -> dict[str, str]:
    with open(file_name, 'r', encoding="utf-8") as file:
        curencies = json.load(file) # maybe error
    return curencies
