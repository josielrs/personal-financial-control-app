from repository.creditCardFlagRepository import searchAllCreditCardFlag
from typing import List
from model.credit_card_flag import CreditCardFlag

def searchAllCreditCardFlags() -> List[CreditCardFlag]:
    return searchAllCreditCardFlag()