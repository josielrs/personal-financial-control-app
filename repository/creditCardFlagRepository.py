from conf.db_session import create_session
from model.credit_card_flag import CreditCardFlag
from typing import List

def searchAllCreditCardFlag() -> List[CreditCardFlag]:

    Session = create_session()
    with Session() as session:
        return session.query(CreditCardFlag).all()

def searchCreditCardFlagById(id: int) -> CreditCardFlag:

    Session = create_session()
    with Session() as session:
        return session.query(CreditCardFlag).filter(CreditCardFlag.id == id).first()