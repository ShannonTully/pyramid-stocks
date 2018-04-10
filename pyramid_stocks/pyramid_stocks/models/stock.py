from sqlalchemy import (
    Column,
    Integer,
    String,
)

from .meta import Base


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False, unique=True)
    companyName = Column(String)
    exchange = Column(String)
    industry = Column(String)
    website = Column(String)
    description = Column(String)
    ceo = Column(String)
    issueType = Column(String)
    sector = Column(String)
