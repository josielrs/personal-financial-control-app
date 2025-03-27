from model.credit_card_flag import CreditCardFlag
from pydantic import BaseModel
from typing import List


class CreditCardFlagSchema(BaseModel):
    id: int
    name: str

    def __str__(self):
        return str(self.__dict__)     


class CreditCardFlagCollectionSchema(BaseModel):
    creditCardFlags: List[CreditCardFlagSchema]

    def __str__(self):
        return str(self.__dict__)


def showCreditCardFlagSchema(creditCardFlag: CreditCardFlag) -> CreditCardFlagSchema:
    
    return {"id":creditCardFlag.id,
            "name":creditCardFlag.name}