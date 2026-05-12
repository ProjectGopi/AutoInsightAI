from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy import Text


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)

    analysis_status = Column(String, default="uploaded")
    analysis_result = Column(Text, nullable=True)
    powerbi_result = Column(Text, nullable=True)