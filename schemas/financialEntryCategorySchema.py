from model.financial_entry_category import FinancialEntryCategory
from pydantic import BaseModel, Field
from typing import List


class FinancialEntryCategorySchema(BaseModel):
    id: int = Field(description="ID da categoria da movimentação financeira.")
    name: str = Field(description="Nome da categoria da movimentação financeira.")

    def __str__(self):
        return str(self.__dict__)     


class FinancialEntryCategorySchemaToSearch(BaseModel):
    entry_type_id: int = Field(description="ID do tipo de movimentação financeira para buscar respectivas categorias, 1 para RECEITA, 2 para DESPESA e 3 para RESERVA")

    def __str__(self):
        return str(self.__dict__)    
    

class FinancialEntryCategoryCollectionSchema(BaseModel):
    financialEntryCategories: List[FinancialEntryCategorySchema] = Field(description="Lista de categoria de movimentação financeira.")

    def __str__(self):
        return str(self.__dict__)
    

def showFinancialEntryCategorySchema(financialEntryCategory: FinancialEntryCategory):
    
    return {"id":financialEntryCategory.id,"name":financialEntryCategory.name}    