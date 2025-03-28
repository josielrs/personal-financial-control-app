from conf.db_session import create_session
from sqlalchemy.sql import text
from model.credit_card import CreditCard
from typing import List
from service.exception.businessRulesException import BusinessRulesException


def hasFinancialEntriesWithCreditCard(number:int) -> int:

    Session = create_session()
    with Session() as session:
        result = session.execute(text('SELECT COUNT(ID) FROM FINANCIAL_ENTRY WHERE CREDIT_CARD_NUMBER='+number))
        if (result):
            for elem in result:
                if (elem[0] and elem[0] > 0):
                    return elem[0]
        
        return 0

def getNextTableId() -> int:

    Session = create_session()
    with Session() as session:
        result = session.execute(text('SELECT MAX(ID) FROM CREDIT_CARD'))
        if (result):
            for elem in result:
                if (elem[0]):
                    return elem[0] + 1
        
        return 1

def insertCreditCard(name: str, 
                     number: int, 
                     month: int, 
                     year: int, 
                     creditFlagId: int) -> None:
    
    newCreditCard : CreditCard = CreditCard()
    newCreditCard.id = getNextTableId()
    newCreditCard.name = name
    newCreditCard.number = number
    newCreditCard.valid_month_date = month
    newCreditCard.valid_year_date = year
    newCreditCard.credit_card_flag_id = creditFlagId

    Session = create_session()
    with Session() as session:
        session.add(newCreditCard)
        session.commit()


def searchCreditCardByNumber(number: int) -> CreditCard:

    Session = create_session()
    with Session() as session:
        return session.query(CreditCard).filter(CreditCard.number == number).first()
    

def searchCreditCardById(id: int) -> CreditCard:

    Session = create_session()
    with Session() as session:
        return session.query(CreditCard).filter(CreditCard.id == id).first()
    

def searchAllCreditCard() -> List[CreditCard]:

    Session = create_session()
    with Session() as session:
        return session.query(CreditCard).all()
    

def updateCreditCard(name: str, 
                     number: int, 
                     month: int, 
                     year: int, 
                     creditFlagId: int) -> None:
    
    Session = create_session()
    with Session() as session:

        existingCreditCard : CreditCard = session.query(CreditCard).filter(CreditCard.number == number).first()

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

        session.commit()


def deleteCreditCard(number: int):

    Session = create_session()
    with Session() as session:
        session.query(CreditCard).filter(CreditCard.number == number).delete()  
        session.commit() 