import sqlalchemy as sa
import sqlalchemy.orm as orm
from datetime import date
from model.base import Base
from model.entry_type import EntryType
from model.value_type import ValueType
from model.financial_entry_category import FinancialEntryCategory
from model.credit_card import CreditCard

def calculateMonthNumber(d1:date, d2:date) -> int:

    if (not d1 or not d2):
        return 0
    
    return (d2.year - d1.year) * 12 + (d2.month - d1.month)

class FinancialEntry(Base):
    __tablename__: str = 'FINANCIAL_ENTRY'

    id: int = sa.Column(sa.Numeric(16), primary_key=True, autoincrement=False, nullable=False)
    name: str = sa.Column(sa.String(256), nullable=False)

    entry_type_id: int = sa.Column(sa.Numeric(16), sa.ForeignKey('ENTRY_TYPE.ID'), nullable=False)
    entry_type: orm.Mapped[EntryType] = orm.relationship('EntryType',lazy='joined')

    recurrent: int = sa.Column(sa.Numeric(1),nullable=False)
    start_date: date = sa.Column(sa.Date,default=date.today,nullable=False)
    finish_date: date = sa.Column(sa.Date,nullable=True)
    value: float = sa.Column(sa.DECIMAL(16,4),nullable=True)

    financial_entry_category_id: int = sa.Column(sa.Numeric(16), sa.ForeignKey('FINANCIAL_ENTRY_CATEGORY.ID'), nullable=False)
    financial_entry_category: orm.Mapped[FinancialEntryCategory] = orm.relationship('FinancialEntryCategory',lazy='joined')

    value_type_id: int = sa.Column(sa.Numeric(16), sa.ForeignKey('VALUE_TYPE.ID'), nullable=False)
    value_type: orm.Mapped[ValueType] = orm.relationship('ValueType',lazy='joined')

    credit_card_id: int = sa.Column(sa.Numeric(16), sa.ForeignKey('CREDIT_CARD.ID'), nullable=True)
    credit_card: orm.Mapped[CreditCard] = orm.relationship('CreditCard',lazy='joined')


    def __str__(self):
        return f'[{'-' if not self.financial_entry_category else self.financial_entry_category.name}] - {self.name} - {self.id}'
    
    
    def returnMonthNumber(self):
        return calculateMonthNumber(self.start_date,self.finish_date)