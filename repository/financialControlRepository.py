from conf.db_session import create_session
from model.financial_control import FinancialControl
from sqlalchemy.sql import text
from typing import List

def insertFinancialControl(month: int, 
                           year: int,
                           status: str) -> None:
    
    newFinancialControl : FinancialControl = FinancialControl()
    newFinancialControl.month = month
    newFinancialControl.year = year
    newFinancialControl.status = status

    Session = create_session()
    with Session() as session:
        session.add(newFinancialControl)
        session.commit()


def searchFinancialControlByMonthAndYear(month: int, year: int) -> FinancialControl:

    Session = create_session()
    with Session() as session:
        return session.query(FinancialControl).filter(FinancialControl.year == year).filter(FinancialControl.month == month).first()


def searchFinancialControlByInitialMonthAndYear(month: int, year: int) -> List[FinancialControl]:

    Session = create_session()
    with Session() as session:
        return session.query(FinancialControl).filter(FinancialControl.year >= year).filter(FinancialControl.month >= month).order_by(FinancialControl.month.asc(),FinancialControl.year.asc()).all()


def searchAllFinancialControl() -> List[FinancialControl]:

    Session = create_session()
    with Session() as session:
        return session.query(FinancialControl).order_by(FinancialControl.month.asc(),FinancialControl.year.asc()).all()


def searchAllFinancialControlWithNoEntries() -> List[FinancialControl]:

    returnValueList: List[FinancialControl] = []

    Session = create_session()
    with Session() as session:
        result = session.execute(text('SELECT FC.MONTH,FC.YEAR FROM FINANCIAL_CONTROL FC WHERE NOT EXISTS (SELECT 1 FROM FINANCIAL_CONTROL_ENTRY FCE WHERE FCE.FINANCIAL_CONTROL_MONTH = FC.MONTH AND FCE.FINANCIAL_CONTROL_YEAR = FC.YEAR)'))
        if (result):
            for elem in result:
                if (elem[0] and elem[1]):
                    month:int = elem[0]
                    year:int = elem[1]
                    returnValueList.append(searchFinancialControlByMonthAndYear(month,year))
        
        return returnValueList


def updateFinancialControlEntry(month: int, 
                                year: int,
                                status: str) -> None:
    
    Session = create_session()
    with Session() as session:    
        existingFinancialControl : FinancialControl = session.query(FinancialControl).filter(FinancialControl.year == year).filter(FinancialControl.month == month).first()
        if (not existingFinancialControl):
            raise RuntimeError(f'Financial Control not found with month:{month} year:{year}')

        existingFinancialControl.status = status

        session.commit()


def deleteFinancialControl(month: int, 
                           year: int) -> None:
    
    Session = create_session()
    with Session() as session:
        session.query(FinancialControl).filter(FinancialControl.year == year).filter(FinancialControl.month == month).delete()  
        session.commit()    


def searchSumaryValueOfGivenEntryTypeIdByMonthAndYear(month:int,year:int,entryTypeId:int) -> float:

    Session = create_session()
    with Session() as session:
        result = session.execute(text(f'SELECT SUM(FCE.VALUE) FROM FINANCIAL_ENTRY FE, FINANCIAL_CONTROL_ENTRY FCE WHERE FCE.FINANCIAL_CONTROL_MONTH = {month} AND FCE.FINANCIAL_CONTROL_YEAR = {year} AND FE.ID = FCE.FINANCIAL_ENTRY_ID AND FE.ENTRY_TYPE_ID = {entryTypeId}'))
        if (result):
            for elem in result:
                if (elem[0]):
                    return elem[0]
        
        return 0   