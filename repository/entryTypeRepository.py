from conf.db_session import create_session
from model.entry_type import EntryType
from typing import List

def searchAllEntryType() -> List[EntryType]:

    Session = create_session()
    with Session() as session:
        return session.query(EntryType).all()