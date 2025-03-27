from model.credit_card import CreditCard
from model.credit_card_flag import CreditCardFlag
from pydantic import BaseModel
from typing import List


class CreditCardSchemaToInsert(BaseModel):
    name: str
    number: int
    valid_month_date: int
    valid_year_date: int
    credit_card_flag_id: int

    def __str__(self):
        return str(self.__dict__)    


class CreditCardSchemaToUpdate(BaseModel):
    id: int
    name: str
    number: int
    valid_month_date: int
    valid_year_date: int
    credit_card_flag_id: int

    def __str__(self):
        return str(self.__dict__)


class CreditCardSchemaToSearch(BaseModel):
    number: int

    def __str__(self):
        return str(self.__dict__)    


class CreditCardSchemaToDelete(BaseModel):
    number: int

    def __str__(self):
        return str(self.__dict__)    


class CreditCardSchema(BaseModel):
    id: int
    name: str
    number: int
    valid_month_date: int
    valid_year_date: int
    credit_card_flag_id: int
    credit_card_flag_name: str
    description: str

    def __str__(self):
        return str(self.__dict__)     


class CreditCardCollectionSchema(BaseModel):
    creditCards: List[CreditCardSchema]

    def __str__(self):
        return str(self.__dict__)    


def showCreditCard(creditCard: CreditCard) -> CreditCardSchema:
    
    return {"id":creditCard.id,
            "name":creditCard.name,
            "number":creditCard.number,
            "valid_month_date":creditCard.valid_month_date,
            "valid_year_date":creditCard.valid_year_date,
            "credit_card_flag_id":creditCard.credit_card_flag_id,
            "credit_card_flag_name": '' if not creditCard.credit_card_flag else creditCard.credit_card_flag.name,
            "description":str(creditCard)}


class CreditCardDelSchema(BaseModel):
    message: int