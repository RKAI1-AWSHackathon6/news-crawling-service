from sqlalchemy import Boolean, Column, Integer, String, Float, BigInteger
from database import Base

class NewspaperSite(Base):
    __tablename__ = "newspapersites"
    id = Column(Integer, primary_key=True, index=True)
    source_url = Column(String, unique=True, nullable=False)
    source_rss = Column(String, unique=True, nullable=True)
