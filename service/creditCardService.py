from repository.creditCardRepository import insertCreditCard as insertCreditCardRep
from repository.creditCardRepository import deleteCreditCard as deleteCreditCardRep
from repository.creditCardRepository import updateCreditCard as updateCreditCardRep
from repository.creditCardRepository import searchCreditCardByNumber as searchCreditCardByNumberRep
from repository.creditCardRepository import searchAllCreditCard as searchAllCreditCardRep
from service.creditCardFlagService import searchCreditCardFlagById
from typing import List
from model.credit_card_flag import CreditCardFlag
from model.credit_card import CreditCard
from service.exception.businessRulesException import BusinessRulesException

def insertCreditCard(name: str, 
                     number: int, 
                     month: int, 
                     year: int, 
                     creditFlagId: int) -> CreditCard:
    
    validateCreditCardData(name, number, month, year, creditFlagId, False)
    
    insertCreditCardRep(name,number,month,year,creditFlagId)

    return searchCreditCardByNumber(number)


def searchCreditCardByNumber(number: int) -> CreditCard:

    return searchCreditCardByNumberRep(number)


def searchAllCreditCard() -> List[CreditCard]:

    return searchAllCreditCardRep()


def updateCreditCard(name: str, 
                     number: int, 
                     month: int, 
                     year: int, 
                     creditFlagId: int) -> CreditCard:

    validateCreditCardData(name, number, month, year, creditFlagId, True)
    
    updateCreditCardRep(name, number, month, year, creditFlagId)

    return searchCreditCardByNumber(number)


def deleteCreditCard(number: int):

    if (not number):
        raise RuntimeError('o numero do cartão deve ser informado !!')
    
    existingCreditCard: CreditCard = searchCreditCardByNumber(number)
    if (not existingCreditCard):
        raise RuntimeError(f'Cartão de crédito de numero {number} não existe na base de dados.')

    deleteCreditCardRep(number)


def validateCreditCardData(name: str, 
                     number: int, 
                     month: int, 
                     year: int, 
                     creditFlagId: int,
                     update: bool) -> None:    
    if (not name):
        raise BusinessRulesException('O nome do cartão deve ser informado !!')
    
    if (not number):
        raise BusinessRulesException('o numero do cartão deve ser informado !!')
    
    existingCreditCard: CreditCard = searchCreditCardByNumber(number)
    if ( not existingCreditCard and update ):
        raise BusinessRulesException(f'Cartão de crédito de numero {number} não existe na base de dados.')
    
    if ( existingCreditCard and not update):
        raise BusinessRulesException(f'Cartão de crédito de numero {number} já existe na base de dados.')    
    
    if (not month):
        raise BusinessRulesException('O mês de validade do cartão deve ser informado !!')
    
    if (month < 1 or month > 12):
        raise BusinessRulesException('O mês de validade do cartão está inválido !!')
    
    if (not year):
        raise BusinessRulesException('O ano de validade do cartão deve ser informado !!')
    
    if (year < 1900 or year > 2999):
        raise BusinessRulesException('O ano de validade do cartão está inválido !!')
    
    if (not creditFlagId):
        raise BusinessRulesException('A bandeira do cartão deve ser informada !!')
    
    creditCardFlag: CreditCardFlag = searchCreditCardFlagById(creditFlagId)
    if (not creditCardFlag):
        raise BusinessRulesException('A bandeira do cartão não encontrada !!')