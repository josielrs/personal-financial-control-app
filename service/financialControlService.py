from model.financial_control import FinancialControl
from model.financial_entry import FinancialEntry

from repository.financialControlRepository import insertFinancialControl as insertFinancialControlRep
from repository.financialControlRepository import searchFinancialControlByMonthAndYear as searchFinancialControlByMonthAndYearRep
from repository.financialControlRepository import searchAllFinancialControl as searchAllFinancialControlRep
from repository.financialControlRepository import updateFinancialControlEntry as updateFinancialControlEntryRep
from repository.financialControlRepository import deleteFinancialControl as deleteFinancialControlRep
from repository.financialControlRepository import searchSumaryValueOfGivenEntryTypeIdByMonthAndYear
from repository.financialControlRepository import searchFinancialControlByInitialMonthAndYear as searchFinancialControlByInitialMonthAndYearRep
from repository.financialControlRepository import searchAllFinancialControlWithNoEntries as searchAllFinancialControlWithNoEntriesRep

from service.financialControlEntryService import deleteAllFinancialControlEntriesByMonthAndYear
from service.financialControlEntryService import insertFinancialControlEntry
from service.financialEntryService import searchAllFinancialEntryByGivenMonthAndYear
from service.exception.businessRulesException import BusinessRulesException
from service.domain.controlStatusEnum import ControlStatus
from service.domain.financialControlSummary import FinancialControlSummary
from service.domain.entryTypeEnum import EntryType

from typing import List
from datetime import date

def insertFinancialControl(month: int, 
                           year: int,
                           status: str) -> FinancialControl:
    
    validateFinancialControlData(month,year,status,False)

    financialControl: FinancialControl = searchFinancialControlByMonthAndYear(month,year)
    if (financialControl):
        raise BusinessRulesException(f'Controle financeiro já criado para {financialControl.description}')

    if (not status):
        status: ControlStatus.ABERTO

    insertFinancialControlRep(month,year,status)

    return searchFinancialControlByMonthAndYear(month,year)

def buildFinancialControl(month: int, 
                           year: int) -> None:
    
    insertFinancialControl(month,year,ControlStatus.ABERTO)

    financialEntries:List[FinancialEntry] = searchAllFinancialEntryByGivenMonthAndYear(month,year)

    if (financialEntries and len(financialEntries)>0):

        for financialEntry in financialEntries:
            financialEntryDay:int = financialEntry.start_date.day()
            insertFinancialControlEntry(month,year,financialEntry.id,financialEntry.value,date(year,month,financialEntryDay))

def searchFinancialControlSummary(month: int, year: int) -> FinancialControlSummary:

    if (not month):
        raise BusinessRulesException('Mês do controle mensal deve ser informado !')    
    if (not year):
        raise BusinessRulesException('Ano do controle mensal deve ser informado !')  

    financialControlSummary: FinancialControlSummary = FinancialControlSummary()
    financialControlSummary.month = month
    financialControlSummary.year = year
    financialControlSummary.revenueAmout = searchSumaryValueOfGivenEntryTypeIdByMonthAndYear(month,year,EntryType.RECEITA.value)
    financialControlSummary.expensesAmout = searchSumaryValueOfGivenEntryTypeIdByMonthAndYear(month,year,EntryType.DESPESA.value)
    financialControlSummary.reservesAmount = searchSumaryValueOfGivenEntryTypeIdByMonthAndYear(month,year,EntryType.RESERVA.value)
    financialControlSummary.difference = financialControlSummary.revenueAmout - (financialControlSummary.expensesAmout + financialControlSummary.reservesAmount)

    return financialControlSummary


def searchFinancialControlByMonthAndYear(month: int, year: int) -> FinancialControl:
    
    return searchFinancialControlByMonthAndYearRep(month,year)


def searchFinancialControlByInitialMonthAndYear(month: int, year: int) -> List[FinancialControl]:

    return searchFinancialControlByInitialMonthAndYearRep(month,year)


def searchAllFinancialControl() -> List[FinancialControl]:
    
    return searchAllFinancialControlRep()


def searchAllFinancialControlWithNoEntries() -> List[FinancialControl]:

    return searchAllFinancialControlWithNoEntriesRep()


def updateFinancialControlEntry(month: int, 
                                year: int,
                                status: str) -> None:
    
    validateFinancialControlData(month,year,status,True)
    updateFinancialControlEntryRep(month,year,status)


def deleteFinancialControl(month: int, 
                           year: int) -> None:
    
    deleteAllFinancialControlEntriesByMonthAndYear(month,year)
    deleteFinancialControlRep(month,year)


def validateFinancialControlData(month: int, 
                                year: int,
                                status: str,
                                isUpdate: bool) -> None:
    
    if (not month):
        raise BusinessRulesException('Mês do controle mensal deve ser informado !')    
    if (month < 1 or month > 12):
        raise BusinessRulesException('O mês informado para o controle mensal, está inválido !!')
    if (not year):
        raise BusinessRulesException('Ano do controle mensal deve ser informado !')    
    if (year < 1900 or year > 2999):
        raise BusinessRulesException('O ano informado para o controle mensal, está inválido !!')
    if (isUpdate and not status):
        raise BusinessRulesException('O novo status do controle mensal deve ser informado !!')
    if (status and not ControlStatus.hasValue(status)):
        raise BusinessRulesException('Status informado é inválido !')