from sqlalchemy import Boolean, Column, Integer, String, Float, BigInteger
from database import Base


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    origin_link = Column(String, unique=True, nullable=False)
    source_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    body= Column(String, nullable=False)
    body_image = Column(String, nullable=True)
    tag = Column(String, nullable=True)
    published_timestamp = Column(BigInteger, nullable=True)
    thumbnail_image_link = Column(String, nullable=True)
    created_at = Column(BigInteger, nullable=False)
    author = Column(String, nullable=True)
    description = Column(String, nullable=True)

    
    
    
    
    