from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from hotel.db.models import Base

engine: Engine = None
DBSession = sessionmaker()


def init_db(file: str) -> Engine:
    engine = create_engine(file)
    Base.metadata.bind = engine
    DBSession.bind = engine
    return engine
