from model.financial_entry_category import FinancialEntryCategory

from typing import List


class FinancialEntryCategorySchema():
    id: int
    name: str

    def __str__(self):
        return str(self.__dict__)     


class FinancialEntryCategorySchemaToSearch():
    entry_type_id: int

    def __str__(self):
        return str(self.__dict__)    
    

class FinancialEntryCategoryCollectionSchema():
    financialEntryCategories: List[FinancialEntryCategorySchema]

    def __str__(self):
        return str(self.__dict__)
    

def showFinancialEntryCategorySchema(financialEntryCategory: FinancialEntryCategory) -> FinancialEntryCategorySchema:
    
    financialEntryCategorySchema: FinancialEntryCategorySchema = FinancialEntryCategorySchema()

    financialEntryCategorySchema.id = financialEntryCategory.id
    financialEntryCategorySchema.name = financialEntryCategory.name

    return financialEntryCategorySchema    