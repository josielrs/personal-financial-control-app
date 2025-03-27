from conf.db_session import create_session
from model.financial_entry_category import FinancialEntryCategory
from typing import List

def searchAllFinancialEntryCategory() -> List[FinancialEntryCategory]:

    Session = create_session()
    with Session() as session:
        return session.query(FinancialEntryCategory).all()


def searchFinancialEntryCategoryById(id: int) -> FinancialEntryCategory:

    Session = create_session()
    with Session() as session:
        return session.query(FinancialEntryCategory).filter(FinancialEntryCategory.id == id).first()


def searchFinancialEntryCategoryByEntryTypeId(entryTypeId: int) -> List[FinancialEntryCategory]:

    Session = create_session()
    with Session() as session:
        return session.query(FinancialEntryCategory).filter(FinancialEntryCategory.entry_type_id == entryTypeId).all()