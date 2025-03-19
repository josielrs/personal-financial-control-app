from enum import Enum

class ValueType(Enum):
    FIXO = 1
    VARIAVEL = 2

    @classmethod
    def hasValue(cls, value):
        return value in cls._value2member_map_
