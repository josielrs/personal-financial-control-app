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

def financialControlDescription(this) -> str:
    return f'{months.get(this.month)}/{this.year}'

class FinancialControl(Base):
    __tablename__: str = 'FINANCIAL_CONTROL'

    month: int = sa.Column(sa.Integer, primary_key=True, nullable=False)
    year: int = sa.Column(sa.Integer, primary_key=True, nullable=False)
    description: str = sa.Column(sa.String(4000),default="Controle Mensal")
    status: str = sa.Column(sa.String(256), nullable=False)

    __mapper_args__ = {
        "primary_key":[month, year]
    }  