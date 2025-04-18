from repository.creditCardRepository import insertCreditCard as insertCreditCardRep
from repository.creditCardRepository import deleteCreditCard as deleteCreditCardRep
from repository.creditCardRepository import updateCreditCard as updateCreditCardRep
from repository.creditCardRepository import searchCreditCardByNumber as searchCreditCardByNumberRep
from repository.creditCardRepository import searchAllCreditCard as searchAllCreditCardRep
from repository.creditCardRepository import searchCreditCardById as searchCreditCardByIdRep
from repository.creditCardRepository import hasFinancialEntriesWithCreditCard
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


def searchCreditCardById(id: int) -> CreditCard:

    return searchCreditCardByIdRep(id)


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
    
    if (hasFinancialEntriesWithCreditCard(number) > 0):
        raise BusinessRulesException(f'Cartão de crédito de numero {number} está associado a movimentações financeiras.')

    deleteCreditCardRep(number)


def validateCreditCardData(name: str, 
                     number: int, 
                     month: int, 
                     year: int, 
                     creditFlagId: int,
                     update: bool) -> None:    
    if (not name and not update):
        raise BusinessRulesException('O nome do cartão deve ser informado !!')
    
    if (not number):
        raise BusinessRulesException('o numero do cartão deve ser informado !!')
    
    existingCreditCard: CreditCard = searchCreditCardByNumber(number)
    if ( not existingCreditCard and update ):
        raise BusinessRulesException(f'Cartão de crédito de numero {number} não existe na base de dados.')
    
    if ( existingCreditCard and not update):
        raise BusinessRulesException(f'Cartão de crédito de numero {number} já existe na base de dados.')    
    
    if (not month and not update):
        raise BusinessRulesException('O mês de validade do cartão deve ser informado !!')
    
    if (month and ( month < 1 or month > 12 )):
        raise BusinessRulesException('O mês de validade do cartão está inválido !!')
    
    if (not year and not update):
        raise BusinessRulesException('O ano de validade do cartão deve ser informado !!')
    
    if (year and ( year < 1900 or year > 2999 )):
        raise BusinessRulesException('O ano de validade do cartão está inválido !!')
    
    if (not creditFlagId and not update):
        raise BusinessRulesException('A bandeira do cartão deve ser informada !!')
    
    if (creditFlagId):
        creditCardFlag: CreditCardFlag = searchCreditCardFlagById(creditFlagId)
        if (not creditCardFlag):
            raise BusinessRulesException('A bandeira do cartão não encontrada !!')