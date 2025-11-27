from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator


class SCurrency(BaseModel):
    currency_from: str = Field(max_length=3, min_length=3)
    currency_to: str = Field(max_length=3, min_length=3)
    amount: float = 1

    @field_validator("currency_from", "currency_to")
    @classmethod
    def validate_currency(cls, v):
        # когда импорт вверху происходит циклический импорт
        from app.services.external_api_service import get_currencies_from_json

        currencies = get_currencies_from_json().keys()
        if v.upper() not in currencies:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Выбранный код валюты не найден.",
            )
        return v
