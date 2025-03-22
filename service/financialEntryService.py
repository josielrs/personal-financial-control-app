from repository.financialEntryRepository import insertFinancialEntry as insertFinancialEntryRep
from repository.financialEntryRepository import searchFinancialEntryById as searchFinancialEntryByIdRep
from repository.financialEntryRepository import searchAllFinancialEntry as searchAllFinancialEntryRep
from repository.financialEntryRepository import searchAllFinancialEntryByDates as searchAllFinancialEntryByDatesRep
from repository.financialEntryRepository import searchAllFinancialEntryByType as searchAllFinancialEntryByTypeRep
from repository.financialEntryRepository import updateFinancialEntry as updateFinancialEntryRep
from repository.financialEntryRepository import deleteFinancialEntryById as deleteFinancialEntryByIdRep
from model.financial_entry import FinancialEntry
from model.financial_entry_category import FinancialEntryCategory
from datetime import date
from service.domain.entryTypeEnum import EntryType
from service.domain.valueTypeEnum import ValueType
from service.financialEntryCategoryService import searchFinancialEntryCategoryById
from service.creditCardService import searchCreditCardById
from typing import List
from model.credit_card import CreditCard
from service.exception.businessRulesException import BusinessRulesException


def diff_month(d1:date, d2:date):
    return (d2.year - d1.year) * 12 + (d2.month - d1.month)


def __insertFinancialEntryData__(name:str,
                                entryTypeId:int,
                                recurrent:int,
                                startDate:date,
                                finishDate:date,
                                value:float,
                                financialEntryCategoryId:int,
                                valueTypeId:int,
                                creditCardId:int) -> int :
    
    validateFinancialEntryData(name, entryTypeId, recurrent, startDate, finishDate, value, financialEntryCategoryId, valueTypeId, creditCardId, False)
        
    id: int = insertFinancialEntryRep(name, entryTypeId, recurrent, startDate, finishDate, value, financialEntryCategoryId, valueTypeId, creditCardId)

    """
        TODO: Incluir processo que insere essa entrada nos meses competentes, e abre os meses que n tiverem abertos
    """

    return id    
    

def insertFinancialEntry(name:str,
                         entryTypeId:int,
                         recurrent:int,
                         startDate:date,
                         finishDate:date,
                         value:float,
                         financialEntryCategoryId:int,
                         valueTypeId:int,
                         creditCardId:int) -> FinancialEntry:
      
    id: int = __insertFinancialEntryData__(name, entryTypeId, recurrent, startDate, finishDate, value, financialEntryCategoryId, valueTypeId, creditCardId)

    return searchFinancialEntryById(id)


def insertFinancialEntry(financialEntry: FinancialEntry) -> FinancialEntry:

    if (not financialEntry):
        raise BusinessRulesException('Nenhuma movimentação finaceira foi informada para inserção !')
    
    id: int = __insertFinancialEntryData__(financialEntry.name,financialEntry.entry_type_id, financialEntry.recurrent,financialEntry.start_date,financialEntry.finish_date,
                               financialEntry.value,financialEntry.financial_entry_category_id,financialEntry.value_type_id,financialEntry.credit_card_id,False);

    return searchFinancialEntryById(id)


def searchAllFinancialEntry() -> List[FinancialEntry]:

    return searchAllFinancialEntryRep()


def searchAllFinancialEntryByType(entryTypeId:int) -> List[FinancialEntry]:

    if (not entryTypeId):
        raise BusinessRulesException('Tipo de movimentação finaceira deve ser informado !')
    
    if (entryTypeId and not EntryType.hasValue(entryTypeId)):
        raise BusinessRulesException('Tipo de movimentação financeira inválido !')    

    return searchAllFinancialEntryByTypeRep(entryTypeId)


def searchFinancialEntryById(id:int) -> FinancialEntry:

    if (not id):
        raise BusinessRulesException('Identificador da movimentação finaceira deve ser informado !')

    return searchFinancialEntryByIdRep(id)


def searchAllFinancialEntryByDates(startDate:date, finishDate:date) -> FinancialEntry:

    if (not startDate and not finishDate):
        raise BusinessRulesException('Favor informar um dos parametros de data !!')
    
    if (startDate and finishDate and (startDate > finishDate)):
        raise BusinessRulesException('Data de inicio da movimentação financeira deve ser menor que a data fim !')    

    return searchAllFinancialEntryByDatesRep(startDate,finishDate)


def updateFinancialEntry(id:int,
                         name:str,
                         entryTypeId:int,
                         recurrent:int,
                         startDate:date,
                         finishDate:date,
                         value:float,
                         financialEntryCategoryId:int,
                         valueTypeId:int,
                         creditCardId:int) -> FinancialEntry:
    
    if (not id):
        raise BusinessRulesException('ID da Movimentação Financeira deve ser informado.')
    
    existingFinancialEntry : FinancialEntry = searchFinancialEntryById(id)

    validateFinancialEntryData(name, entryTypeId, recurrent, startDate, finishDate, value, financialEntryCategoryId, valueTypeId, creditCardId, True, existingFinancialEntry, id)

    updateFinancialEntryRep(id,name,entryTypeId,recurrent,startDate,finishDate,value,financialEntryCategoryId,valueTypeId,creditCardId)

    """
        TODO: Reorgaizar entrada nos controles mensais
    """

    return searchFinancialEntryByIdRep(id)


def deleteFinancialEntryById(id:int) -> None:

    if (not id):
        raise BusinessRulesException('Identificador da movimentação finaceira deve ser informado !')
    
    """
        TODO: Tratar os controles mensais abertos com essa movimentacao
    """    

    return deleteFinancialEntryByIdRep(id)


def validateFinancialEntryData(name:str,
                               entryTypeId:int,
                               recurrent:int,
                               startDate:date,
                               finishDate:date,
                               value:float,
                               financialEntryCategoryId:int,
                               valueTypeId:int,
                               creditCardId:int,
                               isUpdate: bool,
                               financialEntry: FinancialEntry,
                               id: int) -> None:
    
    if (isUpdate and not financialEntry):
        raise BusinessRulesException(f'Movimentação Financeira não encontrada com esse identificador:{id}')

    if (not name and not isUpdate):
        raise BusinessRulesException('A movimentação finaceira deve ter um nome associado a ela !')

    if (not entryTypeId and not isUpdate):
        raise BusinessRulesException('O tipo de movimentação finaceira deve ser informado !')

    if (entryTypeId and not EntryType.hasValue(entryTypeId)):
        raise BusinessRulesException('Tipo de movimentação financeira inválido !')
    
    if (entryTypeId and isUpdate and entryTypeId != financialEntry.entry_type_id):
        raise BusinessRulesException('Não é permitido mudar o tipo da movimentação financeira !')
    
    if (not recurrent and not isUpdate):
        raise BusinessRulesException('Informar a recorrencia da movimentação financeira !')   

    if (recurrent and not (recurrent == 0 or recurrent == 1)):
        raise BusinessRulesException('O parametro "recurrent" deve ser 0 (não) ou 1 (sim) !!')

    if (recurrent and isUpdate and recurrent != financialEntry.recurrent):
        raise BusinessRulesException('Não é permitido mudar a recorrencia da movimentação financeira !')          
    
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
    
    if (valueTypeId and isUpdate and valueTypeId != financialEntry.value_type_id):
        raise BusinessRulesException('Não é permitido mudar o tipo de valor da movimentação financeira !')
    
    if (creditCardId):

        if (not EntryType.DESPESA.value == entryTypeId):
            raise BusinessRulesException('Cartão de crédito deve ser informado apenas em movimentações de DESPESA !')

        creditCardObj: CreditCard = searchCreditCardById(creditCardId)
        if (not creditCardObj):
            raise BusinessRulesException('Cartão de crédito informado não encontrado !') 