import json
from typing import Any

import httpx
from fastapi import HTTPException

from app.api.schemas.currency import SCurrency
from app.core.config import ConfigCurrencyExchange


class ExternalAPIService:
    def __init__(self, client: httpx.AsyncClient, headers: dict | None = None):
        if headers is None or headers.get("apikey") is None:
            config = ConfigCurrencyExchange()
            self.headers = {
                "apikey": config.CURRENCY_EXCHANGE_API_KEY.get_secret_value()
            }
        else:
            self.headers = headers
        self.client = client

    async def make_request(
        self, url: str, timeout: float = 60
    ) -> dict[str, int | dict]:
        try:
            response = await self.client.get(url, timeout=timeout, headers=self.headers)
            # Нужно заменить raise_for_status
            # на свою обработку ошибок
            # для более точной информации об ошибках
            response.raise_for_status()  # Проверяет HTTP ошибки (4xx, 5xx)
            return response.json()
        except httpx.HTTPError as e:
            # Ошибки HTTP (4xx, 5xx) - уже обработаны raise_for_status()
            raise HTTPException(
                status_code=422, detail=f"Ошибка внешнего API: {e.response.status_code}"
            )
        except ValueError:  # Если response.json() не сработает
            raise HTTPException(
                status_code=500, detail="Некорректный JSON в ответе от API"
            )

    async def get_currency_exchenge(self, currency: SCurrency) -> dict[str, Any]:
        url = f"https://api.apilayer.com/currency_data/convert?to={currency.currency_to}&from={currency.currency_from}&amount={currency.amount}"
        # redis cash
        return await self.make_request(url)

    async def get_currency_list(self, file_name="currency_list.json") -> dict[str, Any]:
        url = "https://api.apilayer.com/currency_data/list"
        response_data = await self.make_request(url)
        curencies = response_data["currencies"]
        self.update_currencies_json(curencies, file_name=file_name)
        return response_data

    def update_currencies_json(
        self, response_json, file_name="currency_list.json"
    ) -> None:
        # WARNING: возможно Файл может изменяться сразу несколькими запросами
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(response_json, file, ensure_ascii=False, indent=4)
            # WARNING: нужно проверить содержане данных
