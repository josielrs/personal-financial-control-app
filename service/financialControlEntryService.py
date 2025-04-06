from model.financial_control_entry import FinancialControlEntry
from typing import List
from datetime import date

from repository.financialControlEntryRepository import insertFinancialControlEntry as insertFinancialControlEntryRep
from repository.financialControlEntryRepository import searchAllFinancialControlEntryByMonthAndYear as searchAllFinancialControlEntryByMonthAndYearRep
from repository.financialControlEntryRepository import searchAllFinancialControlEntryByInitialMonthAndYearAndEntryId as searchAllFinancialControlEntryByInitialMonthAndYearAndEntryIdRep
from repository.financialControlEntryRepository import searchAllFinancialControlEntryByFinancialEntryId as searchAllFinancialControlEntryByFinancialEntryIdRep
from repository.financialControlEntryRepository import updateFinancialControlEntry as updateFinancialControlEntryRep
from repository.financialControlEntryRepository import deleteFinancialControlEntry as deleteFinancialControlEntryRep
from repository.financialControlEntryRepository import deleteAllFinancialControlEntriesByMonthAndYear as deleteAllFinancialControlEntriesByMonthAndYearRep

from service.exception.businessRulesException import BusinessRulesException

def insertFinancialControlEntry(month: int, 
                                year: int, 
                                financialEntryId: int,
                                value: float,
                                entryDate: date) -> None:
    
    validateFinancialControlEntryDate(month,year,financialEntryId,value,entryDate,False)    
    insertFinancialControlEntryRep(month,year,financialEntryId,value,entryDate)

    
def searchAllFinancialControlEntryByMonthAndYear(month: int, year: int) -> List[FinancialControlEntry]:

    return searchAllFinancialControlEntryByMonthAndYearRep(month,year)


def searchAllFinancialControlEntryByInitialMonthAndYearAndEntryId(month: int, year: int, entryId: int) -> List[FinancialControlEntry]:

    return searchAllFinancialControlEntryByInitialMonthAndYearAndEntryIdRep(month,year,entryId)


def searchAllFinancialControlEntryByFinancialEntryId(financialEntryId: int) -> List[FinancialControlEntry]:

    return searchAllFinancialControlEntryByFinancialEntryIdRep(financialEntryId)


def updateFinancialControlEntry(month: int, 
                                year: int, 
                                financialEntryId: int,
                                value: float,
                                entryDate: date) -> None:   
    
    validateFinancialControlEntryDate(month,year,financialEntryId,value,entryDate,True)
    updateFinancialControlEntryRep(month,year,financialEntryId,value,entryDate)


def deleteFinancialControlEntry(month: int, 
                                year: int, 
                                financialEntryId: int) -> None:
    
    deleteFinancialControlEntryRep(month,year,financialEntryId)


def deleteAllFinancialControlEntriesByMonthAndYear(month: int, 
                                                    year: int) -> None:      
    
    deleteAllFinancialControlEntriesByMonthAndYearRep(month,year)


def validateFinancialControlEntryDate(month: int, 
                                    year: int, 
                                    financialEntryId: int,
                                    value: float,
                                    entryDate: date,
                                    isUpdate: bool) -> None:
    
    if (not month):
        raise BusinessRulesException('Mês deve ser informado para inserir/atualizar uma movimentação financeira a um controle mensal !')
    
    if (month < 1 or month > 12):
        raise BusinessRulesException('O mês informado para inserir/atualizar uma movimentação financeira a um controle mensal, está inválido !!')    

    if (not year):
        raise BusinessRulesException('Ano deve ser informado para inserir/atualizar uma movimentação financeira a um controle mensal !')
    
    if (year < 1900 or year > 2999):
        raise BusinessRulesException('O ano informado para inserir/atualizar uma movimentação financeira a um controle mensal, está inválido !!')  

    if (not financialEntryId):
        raise BusinessRulesException('Para inserir/atualizar uma movimentação financeira a um controle mensal deve-se informar o ID da movimentação !')
    
    if (not isUpdate and not entryDate):
        raise BusinessRulesException('Para inserir uma movimentação financeira a um controle mensal deve-se informar a data da movimentação !')    