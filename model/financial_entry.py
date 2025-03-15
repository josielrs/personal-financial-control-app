import sqlalchemy as sa
import sqlalchemy.orm as orm
from datetime import date
from model.base import Base
from model.entry_type import EntryType
from model.value_type import ValueType
from model.financial_entry_category import FinancialEntryCategory
from model.credit_card import CreditCard

class FinancialEntry(Base):
    __tablename__: str = 'FINANCIAL_ENTRY'

    id: int = sa.Column(sa.Numeric(16), primary_key=True, autoincrement=True, nullable=False)
    name: str = sa.Column(sa.String(256), nullable=False)

    entry_type_id: int = sa.Column(sa.Numeric(16), sa.ForeignKey('ENTRY_TYPE.ID'), nullable=False)
    entry_type: EntryType = orm.relationship('EntryType',lazy='joined')

    recurrent: int = sa.Column(sa.Numeric(1),nullable=False)
    start_date: date = sa.Column(sa.Date,default=date.now,nullable=False)
    finish_date: date = sa.Column(sa.Date,nullable=True)
    value: float = sa.Column(sa.DECIMAL(16,4),nullable=True)

    financial_entry_category_id: int = sa.Column(sa.Numeric(16), sa.ForeignKey('FINANCIAL_ENTRY_CATEGORY.ID'), nullable=False)
    financial_entry_category: FinancialEntryCategory = orm.relationship('FinancialEntryCategory',lazy='joined')

    value_type_id: int = sa.Column(sa.Numeric(16), sa.ForeignKey('VALUE_TYPE.ID'), nullable=False)
    value_type: ValueType = orm.relationship('ValueType',lazy='joined')

    credit_card_id: int = sa.Column(sa.Numeric(16), sa.ForeignKey('CREDIT_CARD.ID'), nullable=True)
    credit_card: CreditCard = orm.relationship('CreditCard',lazy='joined')



