import sqlalchemy as sa
from model.base import Base

months = {
    1: "JANEIRO",
    2: "FEVEREIRO",
    3: "MARÇO",
    4: "ABRIL",
    5: "MAIO",
    6: "JUNHO",
    7: "JULHO",
    8: "AGOSTO",
    9: "SETEMBRO",
    10: "OUTUBRO",
    11: "NOVEMBRO",
    12: "DEZEMBRO"
}

def financialControlDescription(m:int,y:int) -> str:
        return f'{months.get(m)}/{y}'

class FinancialControl(Base):
    __tablename__: str = 'FINANCIAL_CONTROL'

    month: int = sa.Column(sa.Numeric(2), primary_key=True, autoincrement=False, nullable=False)
    year: int = sa.Column(sa.Numeric(4), primary_key=True, autoincrement=False, nullable=False)
    description: str = sa.Column(sa.String(4000),default=financialControlDescription(month,year))
    status: str = sa.Column(sa.String(256), nullable=False)

    __mapper_args__ = {
        "primary_key":[month, year]
    }  