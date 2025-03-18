from conf.db_session import create_session
from model.credit_card_flag import CreditCardFlag
from typing import List

def searchAllCreditCardFlag() -> List[CreditCardFlag]:

    return create_session().query(CreditCardFlag).all()