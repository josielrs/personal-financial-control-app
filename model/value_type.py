import sqlalchemy as sa
from model.base import Base

class ValueType(Base):
    __tablename__: str = 'VALUE_TYPE'

    id: int = sa.Column(sa.BigInteger, primary_key=True, nullable=False)
    name: str = sa.Column(sa.String(256), nullable=False)
    