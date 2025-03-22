from conf.db_session import create_session
from model.financial_control import FinancialControl
from typing import List

def insertFinancialControl(month: int, 
                           year: int,
                           status: str) -> None:
    
    newFinancialControl : FinancialControl = FinancialControl()
    newFinancialControl.month = month
    newFinancialControl.year = year
    newFinancialControl.status = status

    create_session().add(newFinancialControl)
    create_session().commit

def searchFinancialControlByMonthAndYear(month: int, year: int) -> FinancialControl:

    return create_session().query(FinancialControl).filter(FinancialControl.year == year).filter(FinancialControl.month == month).first()


def searchFinancialControlByInitialMonthAndYear(month: int, year: int) -> List[FinancialControl]:

    return create_session().query(FinancialControl).filter(FinancialControl.year >= year).filter(FinancialControl.month >= month).first()


def searchAllFinancialControl() -> List[FinancialControl]:

    return create_session().query(FinancialControl).all()


def searchAllFinancialControlWithNoEntries() -> List[FinancialControl]:

    returnValueList: List[FinancialControl] = []

    result = create_session().execute(f'SELECT FC.MONTH,FC.YEAR FROM FINANCIAL_CONTROL FC WHERE NOT EXISTS (SELECT 1 FROM FINANCIAL_CONTROL_ENTRY FCE WHERE FCE.FINANCIAL_CONTROL_MONTH = FC.MONTH AND FCE.FINANCIAL_CONTROL_YEAR = FC.YEAR)')
    if (result):
        for elem in result:
            month:int = elem[0]
            year:int = elem[1]
            returnValueList.append(searchFinancialControlByMonthAndYear(month,year))
    
    return returnValueList


def updateFinancialControlEntry(month: int, 
                                year: int,
                                status: str) -> None:
    
    existingFinancialControl : FinancialControl = searchFinancialControlByMonthAndYear(month,year)
    if (not existingFinancialControl):
        raise RuntimeError(f'Financial Control not found with month:{month} year:{year}')

    existingFinancialControl.status = status

    create_session().commit

def deleteFinancialControl(month: int, 
                           year: int) -> None:
    create_session().query(FinancialControl).filter(FinancialControl.year == year).filter(FinancialControl.month == month).delete()  
    create_session().commit    


def searchSumaryValueOfGivenEntryTypeIdByMonthAndYear(month:int,year:int,entryTypeId:int) -> float:

    result = create_session().execute(f'SELECT SUM(FCE.VALUE) FROM FINANCIAL_ENTRY FE, FINANCIAL_CONTROL_ENTRY FCE WHERE FCE.FINANCIAL_CONTROL_MONTH = {month} AND FCE.FINANCIAL_CONTROL_YEAR = {year} AND FE.ID = FCE.FINANCIAL_ENTRY_ID AND FE.VALUE IS NOT NULL AND FE.ENTRY_TYPE_ID = {entryTypeId}')
    if (result):
        for elem in result:
            return elem[0]
    
    return 0   