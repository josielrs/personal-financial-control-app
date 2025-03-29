import sqlalchemy as sa
import sqlalchemy.orm as orm
from model.base import Base
from model.credit_card_flag import CreditCardFlag

class CreditCard(Base):
    __tablename__: str = 'CREDIT_CARD'

    id: int = sa.Column(sa.BigInteger, primary_key=True, nullable=False)
    name: str = sa.Column(sa.String(256), nullable=False)
    number: int = sa.Column(sa.BigInteger, nullable=False)
    valid_month_date: int = sa.Column(sa.Integer, nullable=False)
    valid_year_date: int = sa.Column(sa.Integer, nullable=False)
    credit_card_flag_id: int = sa.Column(sa.BigInteger, sa.ForeignKey('CREDIT_CARD_FLAG.id'), nullable=False)
    credit_card_flag: orm.Mapped[CreditCardFlag] = orm.relationship('CreditCardFlag',lazy='joined')

    def __str__(self):
        return f'[{'-' if not self.credit_card_flag else self.credit_card_flag.name}] - {self.number}'