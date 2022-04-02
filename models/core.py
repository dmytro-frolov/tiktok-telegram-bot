import os
import logging

from contextlib import contextmanager

from sqlalchemy import MetaData, create_engine, Column, Identity, Integer, String
from sqlalchemy.ext.declarative import as_declarative, declarative_base
from sqlalchemy.orm import declared_attr, Session

log = logging.getLogger(__name__)

engine = create_engine(os.environ['DB_URL'])
metadata = MetaData(bind=engine)
# Base.metadata.create_all(engine)

# Base = declarative_base()

@contextmanager
def session(**kwargs):
    new_session = Session(**kwargs)
    try:
        yield new_session
    except Exception as e:
        log.exception(e)
        new_session.rollback()
        raise
    finally:
        new_session.close()


@as_declarative(metadata=metadata)
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, Identity(start=1, cycle=True), primary_key=True)
