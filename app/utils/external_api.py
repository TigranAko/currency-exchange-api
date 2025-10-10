import requests

from app.core.config import ConfigCurrencyExchange

from app.api.schemas.currency import SCurrency
from typing import Any

config = ConfigCurrencyExchange()

payload = {}
headers= {
  "apikey": config.CURRENCY_EXCHANGE_API_KEY.get_secret_value()
}

def get_currency_exchenge(currency: SCurrency) -> dict[str, Any]:
    url = f"https://api.apilayer.com/currency_data/convert?to={currency.currency_to}&from={currency.currency_from}&amount={currency.amount}"


    response = requests.request("GET", url, headers=headers, data = payload)

    status_code = response.status_code
    return {
            "status_code": status_code,
            "json": response.json(),
            "response": response
    }
