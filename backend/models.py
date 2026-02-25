from sqlalchemy import Column, Integer, String, Float
from .database import Base

class ProcessPoint(Base):
    __tablename__ = "ProcessPoints"

    id = Column(Integer, primary_key=True, index=True)
    process_type = Column(String)
    V = Column(Float)
    P = Column(Float)
    T = Column(Float)
    s = Column(Float)
