from model.credit_card import CreditCard
from model.credit_card_flag import CreditCardFlag
from pydantic import BaseModel, Field
from typing import List, Optional


class CreditCardSchemaToInsert(BaseModel):
    name: str = Field(description="Nome designado para o cartão de credito",max_length=256)
    number: int = Field(description="Número do cartão de crédito")
    valid_month_date: int = Field(description="Mês de Validade do Cartão.")
    valid_year_date: int = Field(description="Ano de Validade do Cartão.")
    credit_card_flag_id: int = Field(description="ID da Bandeira do Cartão.")

    def __str__(self):
        return str(self.__dict__)    


class CreditCardSchemaToUpdate(BaseModel):
    name: Optional[str] = Field(default=None,description="Nome a ser alterado ppara o cartão de credito",max_length=256)
    number: int = Field(description="Número do cartão de crédito para alterar.")
    valid_month_date: Optional[int] = Field(default=None,description="Mês de Validade do Cartão a ser alterado.")
    valid_year_date: Optional[int] = Field(default=None,description="Ano de Validade do Cartão a ser alterado.")
    credit_card_flag_id: Optional[int] = Field(default=None,description="ID da Bandeira do Cartão a ser alterado.")

    def __str__(self):
        return str(self.__dict__)


class CreditCardSchemaToSearch(BaseModel):
    number: int = Field(description="Número do cartão de crédito para procurar.")

    def __str__(self):
        return str(self.__dict__)    


class CreditCardSchemaToDelete(BaseModel):
    number: int = Field(description="Número do cartão de crédito para deletar.")

    def __str__(self):
        return str(self.__dict__)    


class CreditCardSchema(BaseModel):
    id: int = Field(description="ID do Cartão de Crédito.")
    name: str = Field(description="Nome designado para o cartão de credito",max_length=256)
    number: int = Field(description="Número do cartão de crédito")
    valid_month_date: int = Field(description="Mês de Validade do Cartão.")
    valid_year_date: int = Field(description="Ano de Validade do Cartão.")
    credit_card_flag_id: int = Field(description="ID da Bandeira do Cartão.")
    credit_card_flag_name: str = Field(description="Nome da Bandeira do Cartão.")
    description: str = Field(description="Descrição do Cartão de Crédito.")

    def __str__(self):
        return str(self.__dict__)     


class CreditCardCollectionSchema(BaseModel):
    creditCards: List[CreditCardSchema] = Field(description="Lista de Cartão de Crédito.")

    def __str__(self):
        return str(self.__dict__)    


def showCreditCard(creditCard: CreditCard):
    
    return {"id":creditCard.id,
            "name":creditCard.name,
            "number":creditCard.number,
            "valid_month_date":creditCard.valid_month_date,
            "valid_year_date":creditCard.valid_year_date,
            "credit_card_flag_id":creditCard.credit_card_flag_id,
            "credit_card_flag_name": '' if not creditCard.credit_card_flag else creditCard.credit_card_flag.name,
            "description":str(creditCard)}


class CreditCardDelSchema(BaseModel):
    message: int