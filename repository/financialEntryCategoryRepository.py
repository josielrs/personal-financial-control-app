from sqlalchemy.orm import Session
from model import Session
from model.financial_entry_category import FinancialEntryCategory
from typing import List

def searchAllFinancialEntryCategory() -> List[FinancialEntryCategory]:

    return Session.query(FinancialEntryCategory).all()


def searchFinancialEntryCategoryById(id: int) -> FinancialEntryCategory:

    return create_session().query(FinancialEntryCategory).filter(FinancialEntryCategory.id == id).first()


def searchFinancialEntryCategoryByEntryTypeId(entryTypeId: int) -> List[FinancialEntryCategory]:

    return create_session().query(FinancialEntryCategory).filter(FinancialEntryCategory.entry_type_id == entryTypeId).all()