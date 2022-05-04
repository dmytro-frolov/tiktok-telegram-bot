import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from models import Base


class User(Base):
    user_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(260))
    created = Column(DateTime, default=datetime.datetime.utcnow)
    tt_links = relationship("CacheLink", backref="user")
