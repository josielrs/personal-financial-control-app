from datetime import date
from model.financial_entry import FinancialEntry
from model.entry_type import EntryType
from model.financial_entry_category import FinancialEntryCategory
from model.value_type import ValueType
from model.credit_card import CreditCard

from typing import List


class FinancialEntrySchemaToInsert():
    name: str
    entry_type_id: int
    recurrent: int
    start_date: date
    finish_date: date
    value: float
    financial_entry_category_id: int
    value_type_id: int
    credit_card_id: int

class FinancialEntrySchemaToUpdate():
    id: int
    start_date: date
    finish_date: date
    value: float
    financial_entry_category_id: int
    credit_card_id: int

class FinancialEntrySchemaToSearch():
    entry_type_id: int

class FinancialEntrySchemaToDelete():
    id: int

class FinancialEntrySchema():
    id: int
    name: str
    entry_type_id: int
    entry_type_name: str
    recurrent: int
    recurrent_desc: str
    start_date: date
    finish_date: date
    value: float
    financial_entry_category_id: int
    financial_entry_category_name: str
    value_type_id: int
    value_type_name: str
    credit_card_id: int
    credit_card_desc: str
    description: str   


class FinancialEntryCollectionSchema():
    financialEntries: List[FinancialEntrySchema]


def showFinancialEntry(financialEntry: FinancialEntry) -> FinancialEntrySchema:
    
    financialEntrySchema: FinancialEntrySchema = FinancialEntrySchema()

    financialEntrySchema.id = financialEntry.id
    financialEntrySchema.name = financialEntry.name
    financialEntrySchema.entry_type_id = financialEntry.entry_type_id
    financialEntrySchema.entry_type_name = financialEntry.entry_type.name if financialEntry.entry_type else ''
    financialEntrySchema.recurrent = financialEntry.recurrent
    financialEntrySchema.recurrent_desc = 'SIM' if financialEntry.recurrent == 1 else 'NÃO'
    financialEntrySchema.start_date = financialEntry.start_date
    financialEntrySchema.finish_date = financialEntry.finish_date
    financialEntrySchema.value = financialEntry.value
    financialEntrySchema.financial_entry_category_id = financialEntry.financial_entry_category_id
    financialEntrySchema.financial_entry_category_name = financialEntry.financial_entry_category.name if financialEntry.financial_entry_category else ''
    financialEntrySchema.value_type_id = financialEntry.value_type_id
    financialEntrySchema.value_type_name = financialEntry.value_type.name if financialEntry.value_type else ''
    financialEntrySchema.credit_card_id = financialEntry.credit_card_id
    financialEntrySchema.credit_card_desc = financialEntry.credit_card.description if financialEntry.credit_card else ''
    financialEntrySchema.description = financialEntry.description

    return financialEntrySchema


class FinancialEntryDelSchema():
    message: int