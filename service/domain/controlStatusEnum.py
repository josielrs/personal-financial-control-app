from enum import Enum

"""
ControlStatus

Objetivo: Determinar o dominio de valores para o status do controle financeiro, FINANCIAL_CONTROL

"""

class ControlStatus(Enum):
    ABERTO = "ABERTO"
    FECHADO = "FECHADO"

    @classmethod
    def hasValue(cls, value) -> bool:
        return value in cls._value2member_map_