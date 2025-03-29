from datetime import date
from pydantic import BaseModel, Field
from model.financial_entry import FinancialEntry
from model.entry_type import EntryType
from model.financial_entry_category import FinancialEntryCategory
from model.value_type import ValueType
from model.credit_card import CreditCard
from typing import Optional

from typing import List


class FinancialEntrySchemaToInsert(BaseModel):
    name: str = Field(description="Nome designado para a movimentação financeira",max_length=256)
    entry_type_id: int = Field(description="ID do tipo de movimentação financeira, 1 para RECEITA, 2 para DESPESA e 3 para RESERVA")
    recurrent: int = Field(description="1 para movimentações recorrentes, 0 pra não recorrentes")
    start_date: date = Field(description="Data da Movimentação")
    finish_date: Optional[date] = Field(default=None,description="Data fim da Movimentação para movimentações recorrentes com data de término.")
    value: Optional[float] = Field(default=None,description="Valor da movimentação financeira")
    financial_entry_category_id: int = Field(description="ID da categoria de movimentação financeira")
    value_type_id: int = Field(description="ID do tipo de valor, 1 para FIXO 2 para VARIAVEL")
    credit_card_number: Optional[int] = Field(default=None,description="Número do cartão de crédito")

    def __str__(self):
        return str(self.__dict__)    


class FinancialEntrySchemaToUpdate(BaseModel):
    id: int = Field(description="ID da Movimentação Financeira que se deseja alterar.")
    name: Optional[str] = Field(default=None,description="Nome a ser alterado para a movimentação financeira",max_length=256)
    start_date: Optional[date] = Field(default=None,description="Data a ser alterada da Movimentação")
    finish_date: Optional[date] = Field(default=None,description="Data Fim a ser alterada da Movimentação")
    value: Optional[float] = Field(default=None,description="Valor a ser alterado da movimentação financeira")
    financial_entry_category_id: Optional[int] = Field(default=None,description="ID da categoria a ser alterada da movimentação financeira")
    credit_card_number: Optional[int] = Field(default=None,description="Número do cartão de crédito a ser alterado da movimentação financeira, -1 se deseja limpar o campo.")

    def __str__(self):
        return str(self.__dict__)


class FinancialEntrySchemaToSearch(BaseModel):
    entry_type_id: int = Field(description="ID do tipo de movimentação financeira a ser procurada, 1 para RECEITA, 2 para DESPESA e 3 para RESERVA")

    def __str__(self):
        return str(self.__dict__)    


class FinancialEntrySchemaToDelete(BaseModel):
    id: int = Field(description="ID da Movimentação Financeira que se deseja excluir.")

    def __str__(self):
        return str(self.__dict__)    


class FinancialEntrySchema(BaseModel):
    id: int = Field(description="ID da Movimentação Financeira.")
    name: str = Field(description="Nome designado para a movimentação financeira")
    entry_type_id: int = Field(description="ID do tipo de movimentação financeira, 1 para RECEITA, 2 para DESPESA e 3 para RESERVA")
    entry_type_name: str = Field(description="Tipo de movimentação financeira")
    recurrent: int = Field(description="1 para movimentações recorrentes, 0 pra não recorrentes")
    recurrent_desc: str = Field(description="Descrição de recorrencia.")
    start_date: date = Field(description="Data da movimentação financeira.")
    finish_date: Optional[date] = Field(default=None,description="Data fim da movimentação financeira, para as recorrentes com data de término.")
    value: Optional[float] = Field(default=None,description="Valor da movimentação financeira, movimentacoes com valor variavel podem não ter valor estipulado neste campo.")
    financial_entry_category_id: int = Field(description="ID da categoria da Movimentação Financeira.")
    financial_entry_category_name: str = Field(description="Nome da categoria da movimentação financeira")
    value_type_id: int = Field(description="ID do tipo de valor, 1 para FIXO 2 para VARIAVEL")
    value_type_name: str = Field(description="Descritivo da tipo de valor da movimentação financeira")
    credit_card_number: Optional[int] = Field(default=None,description="Número do cartão de crédito")
    credit_card_desc: Optional[str] = Field(default=None,description="Nome descritivo do cartão de cŕedito.")
    description: str = Field(description="Descritivo da movimentação financeira.") 

    def __str__(self):
        return str(self.__dict__)     


class FinancialEntryCollectionSchema(BaseModel):
    financialEntries: List[FinancialEntrySchema] = Field(description="Lista de movimentações financeiras.") 

    def __str__(self):
        return str(self.__dict__)    


def showFinancialEntry(financialEntry: FinancialEntry):
    
    return {"id":financialEntry.id,
            "name":financialEntry.name,
            "entry_type_id":financialEntry.entry_type_id,
            "entry_type_name":'' if not financialEntry.entry_type else financialEntry.entry_type.name,
            "recurrent":financialEntry.recurrent,
            "recurrent_desc":'SIM' if financialEntry.recurrent == 1 else 'NÃO',
            "start_date":financialEntry.start_date.strftime('%Y-%m-%d'),
            "finish_date":None if not financialEntry.finish_date else financialEntry.finish_date.strftime('%Y-%m-%d'),
            "value":financialEntry.value,
            "financial_entry_category_id":financialEntry.financial_entry_category_id,
            "financial_entry_category_name": '' if not financialEntry.financial_entry_category else financialEntry.financial_entry_category.name,
            "value_type_id":financialEntry.value_type_id,
            "value_type_name":'' if not financialEntry.value_type else financialEntry.value_type.name,
            "credit_card_number":financialEntry.credit_card_number,
            "credit_card_desc":'' if not financialEntry.credit_card else str(financialEntry.credit_card),
            "description":str(financialEntry)}


class FinancialEntryDelSchema():
    message: int = Field(description="Mensagem de retorno do processamento.") 