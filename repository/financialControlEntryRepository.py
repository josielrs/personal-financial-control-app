from conf.db_session import create_session
from model.financial_control_entry import FinancialControlEntry
from typing import List
from datetime import date

def insertFinancialControlEntry(month: int, 
                                year: int, 
                                financialEntryId: int,
                                value: float,
                                entryDate: date) -> None:
    
    newFinancialControlEntry : FinancialControlEntry = FinancialControlEntry()
    newFinancialControlEntry.financial_control_month = month
    newFinancialControlEntry.financial_control_year = year
    newFinancialControlEntry.financial_entry_id = financialEntryId
    newFinancialControlEntry.value = value
    newFinancialControlEntry.entry_date = entryDate

    create_session().add(newFinancialControlEntry)
    create_session().commit

def searchAllFinancialControlEntryByMonthAndYear(month: int, year: int) -> List[FinancialControlEntry]:

    return create_session().query(FinancialControlEntry).filter(FinancialControlEntry.financial_control_year == year).filter(FinancialControlEntry.financial_control_month == month).all()


def searchAllFinancialControlEntryByInitialMonthAndYearAndEntryId(month: int, year: int, entryId: int) -> List[FinancialControlEntry]:

    return create_session().query(FinancialControlEntry).filter(FinancialControlEntry.financial_control_year >= year).filter(FinancialControlEntry.financial_control_month >= month).filter(FinancialControlEntry.financial_entry_id == entryId).all()


def searchAllFinancialControlEntryByFinancialEntryId(financialEntryId: int) -> List[FinancialControlEntry]:

    return create_session().query(FinancialControlEntry).filter(FinancialControlEntry.financial_entry_id == financialEntryId).all()


def updateFinancialControlEntry(month: int, 
                                year: int, 
                                financialEntryId: int,
                                value: float,
                                entryDate: date) -> None:
    
    existingFinancialControlEntry : FinancialControlEntry = create_session().query(FinancialControlEntry).filter(FinancialControlEntry.financial_control_year == year).filter(FinancialControlEntry.financial_control_month == month).filter(FinancialControlEntry.financial_entry_id == financialEntryId).first()
    if (not existingFinancialControlEntry):
        raise RuntimeError(f'Financial Control Entry not found with month:{month} year:{year} and financialEntryId:{financialEntryId}')

    existingFinancialControlEntry.financial_control_month = month
    existingFinancialControlEntry.financial_control_year = year
    existingFinancialControlEntry.financial_entry_id = financialEntryId
    if (value):
        existingFinancialControlEntry.value = value
    if (entryDate):
        existingFinancialControlEntry.entry_date = entryDate

    create_session().commit

def deleteFinancialControlEntry(month: int, 
                                year: int, 
                                financialEntryId: int) -> None:

    create_session().query(FinancialControlEntry).filter(FinancialControlEntry.financial_control_year == year).filter(FinancialControlEntry.financial_control_month == month).filter(FinancialControlEntry.financial_entry_id == financialEntryId).delete()  
    create_session().commit    

def deleteAllFinancialControlEntriesByMonthAndYear(month: int, 
                                                    year: int) -> None:

    create_session().query(FinancialControlEntry).filter(FinancialControlEntry.financial_control_year == year).filter(FinancialControlEntry.financial_control_month == month).delete()  
    create_session().commit       