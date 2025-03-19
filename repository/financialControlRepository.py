from conf.db_session import create_session
from model.financial_control import FinancialControl
from typing import List
from repository.financialControlEntryRepository import deleteAllFinancialControlEntriesByMonthAndYear

def insertFinancialControl(month: int, 
                           year: int, 
                           description: str,
                           status: str) -> None:
    
    newFinancialControl : FinancialControl = FinancialControl()
    newFinancialControl.month = month
    newFinancialControl.year = year
    newFinancialControl.description = description
    newFinancialControl.status = status

    create_session().add(newFinancialControl)
    create_session().commit

def searchFinancialControlByMonthAndYear(month: int, year: int) -> FinancialControl:

    return create_session().query(FinancialControl).filter(FinancialControl.year == year).filter(FinancialControl.month == month).first()

def searchAllFinancialControl() -> List[FinancialControl]:

    return create_session().query(FinancialControl).all()


def updateFinancialControlEntry(month: int, 
                                year: int, 
                                description: str,
                                status: str) -> None:
    
    existingFinancialControl : FinancialControl = searchFinancialControlByMonthAndYear(month,year)
    if (not existingFinancialControl):
        raise RuntimeError(f'Financial Control not found with month:{month} year:{year}')

    existingFinancialControl.month = month
    existingFinancialControl.year = year
    existingFinancialControl.description = description
    existingFinancialControl.status = status

    create_session().commit

def deleteFinancialControl(month: int, 
                           year: int) -> None:
    deleteAllFinancialControlEntriesByMonthAndYear(month,year)
    create_session().query(FinancialControl).filter(FinancialControl.year == year).filter(FinancialControl.month == month).delete()  
    create_session().commit    