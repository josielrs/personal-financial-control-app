from enum import Enum

class ControlStatus(Enum):
    ABERTO = "ABERTO"
    FECHADO = "FECHADO"

    @classmethod
    def hasValue(cls, value) -> bool:
        return value in cls._value2member_map_