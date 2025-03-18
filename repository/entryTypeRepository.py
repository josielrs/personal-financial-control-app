from conf.db_session import create_session
from model.entry_type import EntryType
from typing import List

def searchAllEntryType() -> List[EntryType]:

    return create_session().query(EntryType).all()