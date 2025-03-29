from model.credit_card_flag import CreditCardFlag
from pydantic import BaseModel, Field
from typing import List


class CreditCardFlagSchema(BaseModel):
    id: int = Field(description="ID da bandeira do cartão.")
    name: str = Field(description="Nome da Bandeira do Cartão.",max_length=256)

    def __str__(self):
        return str(self.__dict__)     


class CreditCardFlagCollectionSchema(BaseModel):
    creditCardFlags: List[CreditCardFlagSchema] = Field(description="Lista de bandeiras de cartões de Crédito.")

    def __str__(self):
        return str(self.__dict__)


def showCreditCardFlagSchema(creditCardFlag: CreditCardFlag) -> CreditCardFlagSchema:
    
    return {"id":creditCardFlag.id,
            "name":creditCardFlag.name}