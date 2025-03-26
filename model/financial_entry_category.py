import sqlalchemy as sa
import sqlalchemy.orm as orm
from model.base import Base
from model.entry_type import EntryType

class FinancialEntryCategory(Base):
    __tablename__: str = 'FINANCIAL_ENTRY_CATEGORY'

    id: int = sa.Column(sa.Numeric(16), primary_key=True, autoincrement=True, nullable=False)
    name: str = sa.Column(sa.String(256), nullable=False)
    entry_type_id: int = sa.Column(sa.Numeric(16), sa.ForeignKey('ENTRY_TYPE.ID'), nullable=False)
