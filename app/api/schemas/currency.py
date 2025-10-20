from pydantic import BaseModel, field_validator, Field

from fastapi import HTTPException, status


class SCurrency(BaseModel):
    currency_from: str = Field(max_length=3, min_length=3)
    currency_to: str = Field(max_length=3, min_length=3)
    amount: float = 1

    @field_validator("currency_from", "currency_to")
    @classmethod
    def validate_currency(cls, v):
        from app.utils.external_api import get_currency_list
        # когда импорт вверху происходит циклический импорт

        currencies = get_currency_list()["json"]["currencies"].keys()
        if v.upper() not in currencies:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Выбранный код валюты не найден.")
        return v

