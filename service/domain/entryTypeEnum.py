from enum import Enum

class EntryType(Enum):
    RECEITA = 1
    DESPESA = 2
    RESERVA = 3

    @classmethod
    def hasValue(cls, value):
        return value in cls._value2member_map_