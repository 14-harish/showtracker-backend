from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base

class UserTVShow(Base):
    __tablename__ = "user_tv_shows"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tv_show_id = Column(Integer, ForeignKey("tv_shows.id"), nullable=False)

    status = Column(String(20), nullable=False)  
    current_season = Column(Integer, nullable=True)
    current_episode = Column(Integer, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
