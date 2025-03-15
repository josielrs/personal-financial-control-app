import sqlalchemy as sa
from model.base import Base

class FinancialControl(Base):
    __tablename__: str = 'FINANCIAL_CONTROL'

    month: int = sa.Column(sa.Numeric(2), primary_key=True, autoincrement=False, nullable=False)
    year: int = sa.Column(sa.Numeric(4), primary_key=True, autoincrement=False, nullable=False)
    description: str = sa.Column(sa.String(4000))
    status: str = sa.Column(sa.String(256), nullable=False)
