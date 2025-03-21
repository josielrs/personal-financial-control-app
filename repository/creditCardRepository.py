from conf.db_session import create_session
from model.credit_card import CreditCard
from typing import List
from service.exception.businessRulesException import BusinessRulesException

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

def searchCreditCardByNumber(number: int) -> CreditCard:

    return create_session().query(CreditCard).filter(CreditCard.number == number).first()

def searchCreditCardById(id: int) -> CreditCard:

    return create_session().query(CreditCard).filter(CreditCard.id == id).first()

def searchAllCreditCard() -> List[CreditCard]:

    return create_session().query(CreditCard).all()

def updateCreditCard(name: str, 
                     number: int, 
                     month: int, 
                     year: int, 
                     creditFlagId: int) -> None:
    
    existingCreditCard : CreditCard = searchCreditCardByNumber(number)
    if (not existingCreditCard):
        raise BusinessRulesException(f'Cartão de crédito não encontrato com o numero {number}')

    if (name):
        existingCreditCard.name = name
    if (number):
        existingCreditCard.number = number
    if (month):
        existingCreditCard.valid_month_date = month
    if (year):
        existingCreditCard.valid_year_date = year
    if (creditFlagId):
        existingCreditCard.credit_card_flag_id = creditFlagId

    create_session().commit

def deleteCreditCard(number: int):

    create_session().query(CreditCard).filter(CreditCard.number == number).delete()  
    create_session().commit    