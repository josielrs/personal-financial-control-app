from enum import Enum

"""
EntryType

Objetivo: Determinar o dominio de valores para o tipo de movimentação financeira na FINANCIAL_ENTRY

"""

class EntryType(Enum):
    RECEITA = 1
    DESPESA = 2
    RESERVA = 3

    @classmethod
    def hasValue(cls, value) -> bool:
        return value in cls._value2member_map_