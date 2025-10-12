import requests

from app.core.config import ConfigCurrencyExchange

from app.api.schemas.currency import SCurrency
from typing import Any
from json import load, dump

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


def get_currency_list() -> dict[str, Any]:
    #Not recommend
    url = "https://api.apilayer.com/currency_data/list"
    response = requests.request("GET", url, headers=headers, data = payload)

    status_code = response.status_code
    return {
            "status_code": status_code,
            "json": response.json(),
            "response": response
    }


def update_currency_json():
    # for admin
    url = "https://api.apilayer.com/currency_data/list"
    response = requests.request("GET", url, headers=headers, data = payload)
    status_code = response.status_code
    text = response.json()

    with open("currency_list.json", 'r', encoding="utf-8") as file:
        old_list = load(file) # maybe error

    with open("currency_list.json", 'w', encoding="utf-8") as file:
        dump(text, file, ensure_ascii=False, indent=4)

    if old_list != text:
        print("\nUPDATING CURRENCY LIST JSON\n")
        print("NEW CURRENCY LIST", text)
        print("\nOLD CURRENCY LIST", old_list)
        print(type(old_list), type(text))
        print()
    else:
        print("Update successfully, and the old data matches the new")

    return {
            "status_code": status_code,
            "json": text,
            "response": response
    }


def get_currencies_from_json() -> dict[str, str]:
    #for users
    with open("currency_list.json", 'r', encoding="utf-8") as file:
        curencies = load(file) # maybe error

    return curencies
