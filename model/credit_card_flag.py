import sqlalchemy as sa
from model.base import Base

class CreditCardFlag(Base):
    __tablename__: str = 'CREDIT_CARD_FLAG'

    id: int = sa.Column(sa.Numeric(16), primary_key=True, autoincrement=True, nullable=False)
    name: str = sa.Column(sa.String(256), nullable=False)
    