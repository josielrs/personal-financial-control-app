from conf.db_session import create_session
from model.value_type import ValueType
from typing import List

def searchAllValueType() -> List[ValueType]:

    return create_session().query(ValueType).all()