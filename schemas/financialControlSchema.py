from datetime import date
from model.financial_control import FinancialControl
from model.financial_control_entry import FinancialControlEntry
from model.financial_entry import FinancialEntry
from pydantic import BaseModel
from schemas.financialEntrySchema import FinancialEntrySchema
from schemas.financialEntrySchema import showFinancialEntry

from service.domain.financialControlSummary import FinancialControlSummary

from typing import List


class FinancialControlSchemaToInsert(BaseModel):
    month: int
    year: int

    def __str__(self):
        return str(self.__dict__)    


class FinancialControlEntrySchemaToUpdate(BaseModel):
    month: int
    year: int
    financialEntryId: int
    value: float

    def __str__(self):
        return str(self.__dict__)


class FinancialControlEntrySchemaToSearch(BaseModel):
    month: int
    year: int

    def __str__(self):
        return str(self.__dict__)    
    
    
class FinancialControlSchemaToSearch(BaseModel):
    month: int
    year: int

    def __str__(self):
        return str(self.__dict__)       


class FinancialControlSchema(BaseModel):
    month: int
    year: int
    description: str

    def __str__(self):
        return str(self.__dict__)     
    

class FinancialControlSummarySchema(BaseModel):
    month: int
    year: int
    revenueAmout: float
    expensesAmout: float
    reservesAmount: float
    difference: float

    def __str__(self):
        return str(self.__dict__) 


class FinancialControlEntrySchema(BaseModel):
    month: int
    year: int
    value: float
    date: date
    financialEntry: FinancialEntrySchema

    def __str__(self):
        return str(self.__dict__) 
    

class FinancialControlCollectionSchema(BaseModel):
    financialControls: List[FinancialControlSchema]

    def __str__(self):
        return str(self.__dict__)  
    

class FinancialControlEntryCollectionSchema(BaseModel):
    financialControlEntries: List[FinancialControlEntrySchema]

    def __str__(self):
        return str(self.__dict__)    


def showFinancialControl(financialControl: FinancialControl) -> FinancialControlSchema:
    
    financialControlSchema: FinancialControlSchema = FinancialControlSchema()

    financialControlSchema.month = financialControl.month  
    financialControlSchema.year = financialControl.year
    financialControlSchema.description = financialControl.description

    return financialControlSchema


def showFinancialControlEntries(financialControlEntry: FinancialControlEntry) -> FinancialControlEntrySchema:
    
    financialControlEntrySchema: FinancialControlEntrySchema = FinancialControlEntrySchema()

    financialControlEntrySchema.month = financialControlEntry.financial_control_month
    financialControlEntrySchema.year = financialControlEntry.financial_control_year
    financialControlEntrySchema.value = financialControlEntry.value
    financialControlEntrySchema.date = financialControlEntry.entry_date
    financialControlEntrySchema.financialEntry = None if not financialControlEntry.financial_entry else showFinancialEntry(financialControlEntry.financial_entry)

    return financialControlEntrySchema


def showFinancialControlSummary(month:int, year:int, financialControlSummary: FinancialControlSummary) -> FinancialControlSummarySchema:

    financialControlSummarySchema: FinancialControlSummarySchema = FinancialControlSummarySchema()

    financialControlSummarySchema.month = month
    financialControlSummarySchema.year = year
    financialControlSummarySchema.revenueAmout = financialControlSummary.revenueAmout
    financialControlSummarySchema.expensesAmout = financialControlSummary.expensesAmout
    financialControlSummarySchema.reservesAmount = financialControlSummary.reservesAmount
    financialControlSummarySchema.difference = financialControlSummary.difference

    return financialControlSummarySchema


class FinancialEntryDelSchema(BaseModel):
    message: int