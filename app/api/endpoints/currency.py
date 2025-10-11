from fastapi import APIRouter, Depends, Response
from app.api.schemas.currency import SCurrency
from app.utils.external_api import get_currency_exchenge, get_currency_list

router = APIRouter(
        prefix="/currency",
        tags=["Currency exchange"]
)

@router.get("/exchange")
def get_currency_exchange_handler(response: Response, currency: SCurrency = Depends()):
    result = get_currency_exchenge(currency)
    response.status_code = result["status_code"]
    print(result)
    return result["json"]


@router.get("/list")
def get_currency_list_handler():
    result = get_currency_list()
    response.status_code = result["status_code"]
    print(result)
    return result["json"]
