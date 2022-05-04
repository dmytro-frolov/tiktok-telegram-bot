import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean

from models import Base


class CacheLink(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    page_url = Column(String(260))
    video_link = Column(String(260))
    created = Column(DateTime, default=datetime.datetime.utcnow)
    archived = Column(Boolean, default=False)
    # shared_times. Create a method for it