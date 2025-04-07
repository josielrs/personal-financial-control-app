from enum import Enum

"""
ValueType

Objetivo: Determinar o dominio de valores para o tipo de valor na movimentação financeira na FINANCIAL_ENTRY, FIXO ou VARIAVEL

"""

class ValueType(Enum):
    FIXO = 1
    VARIAVEL = 2

    @classmethod
    def hasValue(cls, value):
        return value in cls._value2member_map_
