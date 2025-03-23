import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker
from pathlib import Path
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.future.engine import Engine

from model.base import Base

__engine: Optional[Engine] = None

def create_engine() -> Engine:
    """
    Função para criar a conexão com o banco de dados
    """
    global __engine
    
    if __engine:
        return __engine
    
    arquivo_db = 'database/pfcdb.db'
    folder = Path(arquivo_db).parent
    folder.mkdir(parents=True,exist_ok=True)

    conn_str = f'sqlite:///{arquivo_db}'
    __engine = sa.create_engine(url=conn_str, echo=False, connect_args={"check_same_thread": False})

    return __engine

def create_session() -> Session:
    """
    Função para criar a sessao com o banco de dados
    """    
    global __engine

    if not __engine:
        create_engine()

    __session = sessionmaker(__engine, expire_on_commit=False, class_=Session)    

    session: Session = __session

    return session