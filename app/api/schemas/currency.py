from pydantic import BaseModel


class SCurrency(BaseModel):
    currency_from: str
    currency_to: str
    amount: float = 1
