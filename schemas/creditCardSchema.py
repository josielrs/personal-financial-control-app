from model.credit_card import CreditCard
from model.credit_card_flag import CreditCardFlag

from typing import List


class CreditCardSchemaToInsert():
    name: str
    number: int
    valid_month_date: int
    valid_year_date: int
    credit_card_flag_id: int

    def __str__(self):
        return str(self.__dict__)    


class CreditCardSchemaToUpdate():
    id: int
    name: str
    number: int
    valid_month_date: int
    valid_year_date: int
    credit_card_flag_id: int

    def __str__(self):
        return str(self.__dict__)


class CreditCardSchemaToSearch():
    number: int

    def __str__(self):
        return str(self.__dict__)    


class CreditCardSchemaToDelete():
    number: int

    def __str__(self):
        return str(self.__dict__)    


class CreditCardSchema():
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


class CreditCardCollectionSchema():
    creditCards: List[CreditCard]

    def __str__(self):
        return str(self.__dict__)    


def showCreditCard(creditCard: CreditCard) -> CreditCardSchema:
    
    creditCardSchema: CreditCardSchema = CreditCardSchema()

    creditCardSchema.id = creditCard.id
    creditCardSchema.name = creditCard.name
    creditCardSchema.number = creditCard.number
    creditCardSchema.valid_month_date = creditCard.valid_month_date
    creditCardSchema.valid_year_date = creditCard.valid_year_date
    creditCardSchema.credit_card_flag_id = creditCard.credit_card_flag_id
    creditCardSchema.credit_card_flag_name = creditCard.credit_card_flag.name if creditCard.credit_card_flag else ''
    creditCardSchema.description = creditCard.description

    return creditCardSchema


class CreditCardDelSchema():
    message: int