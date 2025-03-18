from conf.db_session import create_session
from model.credit_card import CreditCard
from typing import List

def insertCreditCard(name: str, 
                     number: int, 
                     month: int, 
                     year: int, 
                     creditFlagId: int) -> None:
    
    newCreditCard : CreditCard = CreditCard()
    newCreditCard.name = name
    newCreditCard.number = number
    newCreditCard.valid_month_date = month
    newCreditCard.valid_year_date = year
    newCreditCard.credit_card_flag_id = creditFlagId

    create_session().add(newCreditCard)
    create_session().commit

def searchCreditCard(number: int) -> CreditCard:

    return create_session().query(CreditCard).filter(CreditCard.number == number).first()

def searchAllCreditCard() -> List[CreditCard]:

    return create_session().query(CreditCard).all()

def updateCreditCard(name: str, 
                     number: int, 
                     month: int, 
                     year: int, 
                     creditFlagId: int) -> None:
    
    existingCreditCard : CreditCard = searchCreditCard(number)
    if (not existingCreditCard):
        raise RuntimeError('Credit Card not found with number:'+number)

    existingCreditCard.name = name
    existingCreditCard.number = number
    existingCreditCard.valid_month_date = month
    existingCreditCard.valid_year_date = year
    existingCreditCard.credit_card_flag_id = creditFlagId

    create_session().commit

def deleteCreditCard(number: int):

    create_session().query(CreditCard).filter(CreditCard.number == number).delete()  
    create_session().commit    