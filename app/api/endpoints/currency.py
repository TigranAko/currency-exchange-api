from fastapi import APIRouter, Depends, Response
from app.api.schemas.currency import SCurrency
from app.utils.external_api import get_currency_exchenge, get_currency_list, update_currency_json, get_currencies_from_json
from app.core.security import security

router = APIRouter(
        prefix="/currency",
        tags=["Currency exchange"]
)

@router.get("/exchange", dependencies=[Depends(security.access_token_required)])
def get_currency_exchange_handler(response: Response, currency: SCurrency = Depends()):
    result = get_currency_exchenge(currency)
    response.status_code = result["status_code"]
    print(result)
    return result["json"]


@router.get("/list", description="Not recommend", dependencies=[Depends(security.access_token_required)])
def get_currency_list_handler(response: Response):
    result = get_currency_list()
    response.status_code = result["status_code"]
    print(result)
    return result["json"]


@router.get("/update_list_json", dependencies=[Depends(security.access_token_required)])
def update_currency_file_handler(response: Response):
    result = update_currency_json()
    response.status_code = result["status_code"]
    print(result)
    return result["json"]


@router.get("/list_currency")
def get_currency_from_file():
    result = get_currencies_from_json()
    return result
