import sqlalchemy as sa
from model.base import Base

class FinancialEntryCategory(Base):
    __tablename__: str = 'FINANCIAL_ENTRY_CATEGORY'

    id: int = sa.Column(sa.BigInteger, primary_key=True, nullable=False)
    name: str = sa.Column(sa.String(256), nullable=False)
    entry_type_id: int = sa.Column(sa.BigInteger, sa.ForeignKey('ENTRY_TYPE.id'), nullable=False)
