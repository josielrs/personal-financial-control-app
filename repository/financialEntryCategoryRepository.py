from conf.db_session import create_session
from model.financial_entry_category import FinancialEntryCategory
from typing import List

def searchAllFinancialEntryCategory() -> List[FinancialEntryCategory]:

    return create_session().query(FinancialEntryCategory).all()