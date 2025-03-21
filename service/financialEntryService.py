from repository.financialEntryRepository import insertFinancialEntry as insertFinancialEntryRep


from model.financial_entry import FinancialEntry
from model.financial_entry_category import FinancialEntryCategory
from datetime import date
from service.domain.entryTypeEnum import EntryType
from service.domain.valueTypeEnum import ValueType
from service.financialEntryCategoryService import searchFinancialEntryCategoryById
from service.creditCardService import searchCreditCardById


from service.creditCardFlagService import searchCreditCardFlagById
from typing import List
from model.credit_card_flag import CreditCardFlag
from model.credit_card import CreditCard
from service.exception.businessRulesException import BusinessRulesException


def diff_month(d1:date, d2:date):
    return (d2.year - d1.year) * 12 + (d2.month - d1.month)


def insertFinancialEntry(name:str,
                         entryTypeId:int,
                         recurrent:int,
                         startDate:date,
                         finishDate:date,
                         value:float,
                         financialEntryCategoryId:int,
                         valueTypeId:int,
                         creditCardId:int) -> FinancialEntry:
    
    validateFinancialEntryData(name, entryTypeId, recurrent, startDate, finishDate, value, financialEntryCategoryId, valueTypeId, creditCardId, False)




    return


def insertFinancialEntry(financialEntry: FinancialEntry) -> None:

    return


def searchAllFinancialEntry() -> List[FinancialEntry]:

    return


def searchAllFinancialEntryByType(entryTypeId:int) -> List[FinancialEntry]:

    return


def searchFinancialEntryById(id:int) -> FinancialEntry:

    return


def searchAllFinancialEntryByDates(startDate:date, finishDate:date) -> FinancialEntry:

    return query.all()


def updateFinancialEntry(id:int,
                         name:str,
                         entryTypeId:int,
                         recurrent:int,
                         startDate:date,
                         finishDate:date,
                         value:float,
                         financialEntryCategoryId:int,
                         valueTypeId:int,
                         creditCardId:int) -> None:
    
    validateFinancialEntryData(name, entryTypeId, recurrent, startDate, finishDate, value, financialEntryCategoryId, valueTypeId, creditCardId, False)

    return


def deleteFinancialControlEntryById(id:int) -> None:

    return


def validateFinancialEntryData(name:str,
                               entryTypeId:int,
                               recurrent:int,
                               startDate:date,
                               finishDate:date,
                               value:float,
                               financialEntryCategoryId:int,
                               valueTypeId:int,
                               creditCardId:int,
                               isUpdate: bool) -> None:
    if (not name and not isUpdate):
        raise BusinessRulesException('A movimentação finaceira deve ter um nome associado a ela !')

    if (not entryTypeId and not isUpdate):
        raise BusinessRulesException('O tipo de movimentação finaceira deve ser informado !')

    if (entryTypeId and not EntryType.hasValue(entryTypeId)):
        raise BusinessRulesException('Tipo de movimentação financeira inválido !')
    
    if (not recurrent and not isUpdate):
        raise BusinessRulesException('Informar a recorrencia da movimentação financeira !')   

    if (recurrent and not (recurrent == 0 or recurrent == 1)):
        raise BusinessRulesException('O parametro "recurrent" deve ser 0 (não) ou 1 (sim) !!')      
    
    if (not startDate and not isUpdate):
        raise BusinessRulesException('Data de inicio da movimentação financeira deve ser informada !')

    if (finishDate and (recurrent == 0)):
        raise BusinessRulesException('Data fim só deve ser informada em movimentações recorrentes !')

    if (finishDate and (startDate > finishDate)):
        raise BusinessRulesException('Data de inicio da movimentação financeira deve ser menor que a data fim !')
    
    if (finishDate and diff_month(startDate,finishDate) <= 0):
        raise BusinessRulesException('Data de inicio e fim da movimentação financeira deve ser ter no minimo 1 mês de diferença !')
           
    if (value and value < 0):
        raise BusinessRulesException('Valor da movimentação financeira não pode ser negativo !') 
    
    if (not financialEntryCategoryId and not isUpdate):
        raise BusinessRulesException('A categoria da movimentação finaceira deve ser informada !')
    
    if (financialEntryCategoryId):
        category:FinancialEntryCategory = searchFinancialEntryCategoryById(financialEntryCategoryId)
        if (not category):
            raise BusinessRulesException('A categoria da movimentação finaceira informada é inválida !')
    
    if (not valueTypeId and not isUpdate):
        raise BusinessRulesException('O tipo de valor da movimentação finaceira deve ser informado !')

    if (valueTypeId and not ValueType.hasValue(valueTypeId)):
        raise BusinessRulesException('Tipo de valor da movimentação financeira inválido !')
    
    if (creditCardId):

        if (not EntryType.DESPESA.value == entryTypeId):
            raise BusinessRulesException('Cartão de crédito deve ser informado apenas em movimentações de DESPESA !')

        creditCardObj: CreditCard = searchCreditCardById(creditCardId)
        if (not creditCardObj):
            raise BusinessRulesException('Cartão de crédito informado não encontrado !')    