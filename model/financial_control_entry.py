import sqlalchemy as sa
import sqlalchemy.orm as orm
from model.base import Base
from model.financial_control import FinancialControl
from model.financial_entry import FinancialEntry

from datetime import date

class FinancialControlEntry(Base):
    __tablename__: str = 'FINANCIAL_CONTROL_ENTRY'

    financial_control_month: int = sa.Column(sa.Integer, nullable=False)
    financial_control_year: int = sa.Column(sa.Integer, nullable=False)

    financial_entry_id: int = sa.Column(sa.Integer, sa.ForeignKey('FINANCIAL_ENTRY.id'), nullable=False)
    financial_entry: orm.Mapped[FinancialEntry] = orm.relationship('FinancialEntry',lazy='joined')

    value: float = sa.Column(sa.DECIMAL(16,2),nullable=True)
    entry_date: date = sa.Column(sa.Date,nullable=False)

    __mapper_args__ = {
        "primary_key":[financial_control_month, financial_control_year, financial_entry_id]
    }    