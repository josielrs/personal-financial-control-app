from conf.db_session import create_session
from model.financial_entry import FinancialEntry
from typing import List
from datetime import date

def insertFinancialEntry(name:str,
                         entryTypeId:int,
                         recurrent:int,
                         startDate:date,
                         finishDate:date,
                         value:float,
                         financialEntryCategoryId:int,
                         valueTypeId:int,
                         creditCardId:int) -> None:
    
    newFinancialEntry : FinancialEntry = FinancialEntry()
    newFinancialEntry.name = name
    newFinancialEntry.entry_type_id = entryTypeId
    newFinancialEntry.recurrent = recurrent
    newFinancialEntry.start_date = startDate
    newFinancialEntry.finish_date = finishDate
    newFinancialEntry.value = value
    newFinancialEntry.financial_entry_category_id = financialEntryCategoryId
    newFinancialEntry.value_type_id = valueTypeId
    newFinancialEntry.credit_card_id = creditCardId

    create_session().add(newFinancialEntry)
    create_session().commit


def insertFinancialEntry(financialEntry: FinancialEntry) -> None:

    create_session().add(financialEntry)
    create_session().commit


def searchAllFinancialEntry() -> List[FinancialEntry]:

    return create_session().query(FinancialEntry).all()


def searchAllFinancialEntryByType(entryTypeId:int) -> List[FinancialEntry]:

    return create_session().query(FinancialEntry).filter(FinancialEntry.entry_type_id == entryTypeId).all()


def searchFinancialEntryById(id:int) -> FinancialEntry:

    return create_session().query(FinancialEntry).filter(FinancialEntry.id == id).first()


def searchAllFinancialEntryByDates(startDate:date, finishDate:date) -> FinancialEntry:

    query = create_session().query(FinancialEntry)

    if startDate:
        query.filter(FinancialEntry.start_date >= startDate)

    if finishDate:
        query.filter(FinancialEntry.finish_date <= finishDate or FinancialEntry.finish_date is None)     

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
    
    if (not id):
        raise RuntimeError('id must be given to update Financial Entry record.')
    
    existingFinancialEntry : FinancialEntry = searchFinancialEntryById(id)

    if (not existingFinancialEntry):
        raise RuntimeError(f'Financial Entry not found with ID:{id}')

    if (name):
        existingFinancialEntry.name = name
    if (entryTypeId):        
        existingFinancialEntry.entry_type_id = entryTypeId
    if (recurrent):
        existingFinancialEntry.recurrent = recurrent
    if (startDate):        
        existingFinancialEntry.start_date = startDate
    if (finishDate):    
        existingFinancialEntry.finish_date = finishDate
    if (value):        
        existingFinancialEntry.value = value
    if (financialEntryCategoryId):    
        existingFinancialEntry.financial_entry_category_id = financialEntryCategoryId
    if (valueTypeId):        
        existingFinancialEntry.value_type_id = valueTypeId
    if (creditCardId):        
        existingFinancialEntry.credit_card_id = creditCardId

    create_session().commit


def deleteFinancialControlEntryById(id:int) -> None:

    create_session().query(FinancialEntry).filter(FinancialEntry.id == id).delete()
    create_session().commit     