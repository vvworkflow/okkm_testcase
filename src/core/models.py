from pydantic import BaseModel
from sqlalchemy import Column, Integer, SmallInteger, Numeric, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class PercentResponse(BaseModel):
    percent: float

class RespondentsData(Base):
    __tablename__ = "respondentsdata"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    respondent = Column(Integer, nullable=False)
    sex = Column(SmallInteger)
    age = Column(Integer)
    weight = Column(Numeric)
