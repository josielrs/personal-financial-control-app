from repository.financialEntryCategoryRepository import searchAllFinancialEntryCategory as searchAllFinancialEntryCategoryRep
from repository.financialEntryCategoryRepository import searchFinancialEntryCategoryById as searchFinancialEntryCategoryByIdRep
from typing import List
from model.financial_entry_category import FinancialEntryCategory

def searchAllFinancialEntryCategory() -> List[FinancialEntryCategory]:

    return searchAllFinancialEntryCategoryRep()


def searchFinancialEntryCategoryById(id: int) -> FinancialEntryCategory:

    return searchFinancialEntryCategoryByIdRep(id)