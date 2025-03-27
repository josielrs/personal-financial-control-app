from conf.db_session import create_session
from model.value_type import ValueType
from typing import List

def searchAllValueType() -> List[ValueType]:

    Session = create_session()
    with Session() as session:
        return session.query(ValueType).all()