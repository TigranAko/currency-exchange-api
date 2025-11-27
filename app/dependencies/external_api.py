import json

from fastapi import Request

from app.services.external_api_service import ExternalAPIService


async def get_external_api_service(request: Request) -> ExternalAPIService:
    return ExternalAPIService(request.app.state.client)


def get_currencies_from_json(file_name="currency_list.json") -> dict[str, str]:
    with open(file_name, "r", encoding="utf-8") as file:
        curencies = json.load(file)  # maybe error
    return curencies
