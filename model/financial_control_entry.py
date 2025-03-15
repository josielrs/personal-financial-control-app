import sqlalchemy as sa
import sqlalchemy.orm as orm
from model.base import Base
from model.financial_control import FinancialControl
from model.financial_entry import FinancialEntry

class FinancialControlEntry(Base):
    __tablename__: str = 'FINANCIAL_CONTROL_ENTRY'

    financial_control_month: int = sa.Column(sa.Numeric(2), sa.ForeignKey('FINANCIAL_CONTROL.month'), nullable=False)
    financial_control_year: int = sa.Column(sa.Numeric(4), sa.ForeignKey('FINANCIAL_CONTROL.year'), nullable=False)
    financial_control: FinancialControl = orm.relationship('FinancialControl',lazy='joined')

    financial_entry_id: int = sa.Column(sa.Numeric(16), sa.ForeignKey('FINANCIAL_ENTRY.ID'), nullable=False)
    financial_entry: FinancialEntry = orm.relationship('FinancialEntry',lazy='joined')

    value: float = sa.Column(sa.DECIMAL(16,4),nullable=True)