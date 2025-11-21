from fastapi import APIRouter, Depends, Response

from app.api.schemas.currency import SCurrency
from app.core.security import security
from app.utils.external_api import (
    get_currencies_from_json,
    get_currency_exchenge,
    get_currency_list,
)

router = APIRouter(prefix="/currency", tags=["Currency exchange"])


@router.get(
    "/exchange",
    description="Convert currencies",
    dependencies=[Depends(security.access_token_required)],
)
def get_currency_exchange_handler(response: Response, currency: SCurrency = Depends()):
    result = get_currency_exchenge(currency)
    response.status_code = result["status_code"]
    print(result)
    return result["json"]


@router.get(
    "/list",
    description="Get currencies and update currency_list.json",
    dependencies=[Depends(security.access_token_required)],
)
def get_currency_list_handler(response: Response):
    result = get_currency_list()
    response.status_code = result["status_code"]
    print(result)
    return result["json"]


@router.get("/list_currency", description="Get curencise from currency_list.json")
def get_currency_from_file():
    result = get_currencies_from_json()
    return result
