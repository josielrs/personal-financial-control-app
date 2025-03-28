import sqlalchemy as sa
from model.base import Base

class EntryType(Base):
    __tablename__: str = 'ENTRY_TYPE'

    id: int = sa.Column(sa.Numeric(16), primary_key=True, nullable=False)
    name: str = sa.Column(sa.String(256), nullable=False)
