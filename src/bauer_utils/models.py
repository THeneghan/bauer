"""SQLalchemy models"""

from sqlalchemy import JSON, BigInteger, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """SQLAlchemy base model"""

    pass


class Attributes(Base):
    """Table to store customer transactions"""

    __tablename__ = "attributes"
    external_id = Column(BigInteger, primary_key=True)
    email = Column(String)


class Events(Base):
    """Table to store GTR data"""

    __tablename__ = "events"
    record_id = Column(BigInteger, primary_key=True)
    external_id = Column(BigInteger, ForeignKey("attributes.external_id"))
    name = Column(String)
    properties = Column(JSON)


class Purchases(Base):
    """Table to store GTR data"""

    __tablename__ = "purchases"
    record_id = Column(BigInteger, primary_key=True)
    external_id = Column(BigInteger, ForeignKey("attributes.external_id"))
    product_id = Column(String)
    time = Column(DateTime)
    currency = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    properties = Column(JSON)
