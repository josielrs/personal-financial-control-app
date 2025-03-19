from repository.creditCardFlagRepository import searchAllCreditCardFlag as searchAllCreditCardFlagRep
from repository.creditCardFlagRepository import searchCreditCardFlagById as searchCreditCardFlagByIdRep
from typing import List
from model.credit_card_flag import CreditCardFlag

def searchAllCreditCardFlag() -> List[CreditCardFlag]:
    return searchAllCreditCardFlagRep()

def searchCreditCardFlagById(id: int) -> CreditCardFlag:
    return searchCreditCardFlagByIdRep(id)