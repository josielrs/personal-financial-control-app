from datetime import date
from model.financial_control import FinancialControl
from model.financial_control import financialControlDescription
from model.financial_control_entry import FinancialControlEntry
from model.financial_entry import FinancialEntry
from pydantic import BaseModel, Field
from schemas.financialEntrySchema import FinancialEntrySchema
from schemas.financialEntrySchema import showFinancialEntry

from service.domain.financialControlSummary import FinancialControlSummary

from typing import List, Optional


class FinancialControlSchemaToInsert(BaseModel):
    month: int = Field(description="Mês de referencia do Controle Financeiro.")
    year: int = Field(description="Ano de referencia do Controle Financeiro.")

    def __str__(self):
        return str(self.__dict__)    


class FinancialControlEntrySchemaToUpdate(BaseModel):
    month: int = Field(description="Mês de referencia do Controle Financeiro que deseja alterar.")
    year: int = Field(description="Ano de referencia do Controle Financeiro que deseja alterar.")
    financialEntryId: int = Field(description="ID da movimentação que deseja alterar.")
    value: float = Field(description="Valor a ser alterado.")

    def __str__(self):
        return str(self.__dict__)


class FinancialControlEntrySchemaToSearch(BaseModel):
    month: int = Field(description="Mês de referencia do Controle Financeiro que deseja busca.")
    year: int = Field(description="Ano de referencia do Controle Financeiro que deseja busca.")

    def __str__(self):
        return str(self.__dict__)    
    
    
class FinancialControlSchemaToSearch(BaseModel):
    month: int = Field(description="Mês de referencia do Controle Financeiro que deseja busca.")
    year: int = Field(description="Ano de referencia do Controle Financeiro que deseja busca.")

    def __str__(self):
        return str(self.__dict__)       


class FinancialControlSchema(BaseModel):
    month: int = Field(description="Mês de referencia do Controle Financeiro.")
    year: int = Field(description="Ano de referencia do Controle Financeiro.")
    description: str = Field(description="Descritivo do Controle Financeiro.")

    def __str__(self):
        return str(self.__dict__)     
    

class FinancialControlSummarySchema(BaseModel):
    description: str = Field(description="Descritivo do Controle Financeiro.")
    month: int = Field(description="Mês de referencia do Controle Financeiro que deseja busca.")
    year: int = Field(description="Ano de referencia do Controle Financeiro que deseja busca.")
    revenueAmout: float = Field(description="Valor total de RECEITAS do mês de referencia.")
    expensesAmout: float = Field(description="Valor total de DESPESAS do mês de referencia.")
    reservesAmount: float = Field(description="Valor total de RESERVAS do mês de referencia.")
    difference: float = Field(description="Valor restante para o mês de referencia. RECEITAS - (DESPESAS + RESERVAS)")
    reservesPercent: int = Field(description="percentual da reserva em cima das receitas")

    def __str__(self):
        return str(self.__dict__) 


class FinancialControlEntrySchema(BaseModel):
    month: int = Field(description="Mês de referencia da movimentação no controle financeiro.")
    year: int = Field(description="Ano de referencia da movimentação no controle financeiro.")
    value: float = Field(description="Valor da movimentação no controle financeiro.")
    entryDate: date = Field(description="Data da movimentação no controle financeiro.")
    financialEntry: FinancialEntrySchema = Field(description="Dados da movimentação financeira.")

    def __str__(self):
        return str(self.__dict__) 
    

class FinancialControlCollectionSchema(BaseModel):
    financialControls: List[FinancialControlSchema] = Field(description="Lista de controles financeiros.")

    def __str__(self):
        return str(self.__dict__)  
    

class FinancialControlEntryCollectionSchema(BaseModel):
    financialControlEntries: List[FinancialControlEntrySchema] = Field(description="Lista de movimentações do mes/ano de referencia do controle financeiro.")

    def __str__(self):
        return str(self.__dict__)    


def showFinancialControl(financialControl: FinancialControl) -> FinancialControlSchema:
    
    return {"month":financialControl.month,
            "year":financialControl.year,
            "description":financialControlDescription(financialControl)}


def showFinancialControlEntries(financialControlEntry: FinancialControlEntry) -> FinancialControlEntrySchema:
    
    return {"month":financialControlEntry.financial_control_month,
            "year":financialControlEntry.financial_control_year,
            "value":financialControlEntry.value,
            "entryDate":financialControlEntry.entry_date.strftime('%Y-%m-%d'),
            "financialEntry":'' if not financialControlEntry.financial_entry else showFinancialEntry(financialControlEntry.financial_entry)}


def showFinancialControlSummary(month:int, year:int, financialControlSummary: FinancialControlSummary):
    
    financialControl: FinancialControl = FinancialControl()
    financialControl.month = month
    financialControl.year = year

    return {"description":financialControlDescription(financialControl),
            "month":month,
            "year":year,
            "revenueAmout":financialControlSummary.revenueAmout,
            "expensesAmout":financialControlSummary.expensesAmout,
            "reservesAmount":financialControlSummary.reservesAmount,
            "difference":financialControlSummary.difference,
            "reservesPercent":financialControlSummary.reservesPercent}


class FinancialEntryDelSchema(BaseModel):
    message: int = Field(description="Mensagem de retorno do processamento.") 