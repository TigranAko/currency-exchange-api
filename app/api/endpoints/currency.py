from fastapi import APIRouter, Depends, Response

from app.api.schemas.currency import SCurrency
from app.core.security import security
from app.dependencies.external_api import (
    get_currencies_from_json,
    get_external_api_service,
)
from app.services.external_api_service import ExternalAPIService

router = APIRouter(prefix="/currency", tags=["Currency exchange"])


@router.get(
    "/exchange",
    description="Convert currencies",
    dependencies=[Depends(security.access_token_required)],
)
async def get_currency_exchange_handler(
    response: Response,
    currency: SCurrency = Depends(),
    eapi_service: ExternalAPIService = Depends(get_external_api_service),
):
    result = await eapi_service.get_currency_exchenge(currency)
    return result


@router.get(
    "/list",
    description="Get currencies and update currency_list.json",
    dependencies=[Depends(security.access_token_required)],
)
async def get_currency_list_handler(
    response: Response,
    eapi_service: ExternalAPIService = Depends(get_external_api_service),
):
    result = await eapi_service.get_currency_list()
    return result


@router.get("/list_currency", description="Get curencise from currency_list.json")
async def get_currency_from_file():
    result = get_currencies_from_json()
    return result
