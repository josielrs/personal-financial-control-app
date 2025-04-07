from conf.db_session import create_session
from sqlalchemy.sql import text
from sqlalchemy import or_ 
from sqlalchemy import and_
from model.financial_entry import FinancialEntry
from typing import List
from datetime import date
from service.exception.businessRulesException import BusinessRulesException

def getNextTableId() -> int:

    Session = create_session()
    with Session() as session:
        result = session.execute(text('SELECT MAX(ID) FROM FINANCIAL_ENTRY'))
        if (result):
            for elem in result:
                if (elem[0]):
                    return elem[0] + 1
        
        return 1


def insertFinancialEntry(name:str,
                         entryTypeId:int,
                         recurrent:int,
                         startDate:date,
                         finishDate:date,
                         value:float,
                         financialEntryCategoryId:int,
                         valueTypeId:int,
                         creditCardNumber:int) -> int:
    
    createdId:int = getNextTableId()

    newFinancialEntry : FinancialEntry = FinancialEntry()
    newFinancialEntry.id = createdId
    newFinancialEntry.name = name
    newFinancialEntry.entry_type_id = entryTypeId
    newFinancialEntry.recurrent = recurrent
    newFinancialEntry.start_date = startDate
    newFinancialEntry.finish_date = finishDate
    newFinancialEntry.value = value
    newFinancialEntry.financial_entry_category_id = financialEntryCategoryId
    newFinancialEntry.value_type_id = valueTypeId
    newFinancialEntry.credit_card_number = creditCardNumber

    Session = create_session()
    with Session() as session:
        session.add(newFinancialEntry)
        session.commit()

        return createdId


def searchAllFinancialEntry() -> List[FinancialEntry]:

    Session = create_session()
    with Session() as session:
        return session.query(FinancialEntry).all()


def searchAllFinancialEntryByType(entryTypeId:int) -> List[FinancialEntry]:

    Session = create_session()
    with Session() as session:
        return session.query(FinancialEntry).filter(FinancialEntry.entry_type_id == entryTypeId).all()


def searchFinancialEntryById(id:int) -> FinancialEntry:

    Session = create_session()
    with Session() as session:
        return session.query(FinancialEntry).filter(FinancialEntry.id == id).first()


def searchAllFinancialEntryByDates(startDate:date, finishDate:date) -> List[FinancialEntry]:

    Session = create_session()
    with Session() as session:
        query = session.query(FinancialEntry)

        if startDate:
            query.filter(FinancialEntry.start_date >= startDate)

        """ este método retorna as entradas que inicial na data informada e terminam na data informa ou simplemente n tem data fim informada e são recorrentes """
        if finishDate:
            query.filter(or_(FinancialEntry.finish_date <= finishDate,and_(FinancialEntry.finish_date is None, FinancialEntry.recurrent == 1)))     

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
                         creditCardNumber:int) -> None:
    
    if (not id):
        raise BusinessRulesException('ID da Movimentação Financeira deve ser informado.')
    

    Session = create_session()
    with Session() as session:

        existingFinancialEntry : FinancialEntry = session.query(FinancialEntry).filter(FinancialEntry.id == id).first()

        if (not existingFinancialEntry):
            raise BusinessRulesException(f'Movimentação Financeira não encontrada com esse identificador:{id}')

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
        if (creditCardNumber):        
            existingFinancialEntry.credit_card_number = creditCardNumber if creditCardNumber != -1 else None

        session.commit()


def deleteFinancialEntryById(id:int) -> None:

    Session = create_session()
    with Session() as session:
        session.query(FinancialEntry).filter(FinancialEntry.id == id).delete()
        session.commit()     