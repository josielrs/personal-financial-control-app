from model.financial_entry_category import FinancialEntryCategory
from pydantic import BaseModel
from typing import List


class FinancialEntryCategorySchema(BaseModel):
    id: int
    name: str

    def __str__(self):
        return str(self.__dict__)     


class FinancialEntryCategorySchemaToSearch(BaseModel):
    entry_type_id: int

    def __str__(self):
        return str(self.__dict__)    
    

class FinancialEntryCategoryCollectionSchema(BaseModel):
    financialEntryCategories: List[FinancialEntryCategorySchema]

    def __str__(self):
        return str(self.__dict__)
    

def showFinancialEntryCategorySchema(financialEntryCategory: FinancialEntryCategory):
    
    return {"id":financialEntryCategory.id,"name":financialEntryCategory.name}    