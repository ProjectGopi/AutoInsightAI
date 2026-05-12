from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    anomaly_level = Column(String, default="medium")
    auto_analyze = Column(Boolean, default=True)
    default_target = Column(String, nullable=True)
    dark_mode = Column(Boolean, default=False)