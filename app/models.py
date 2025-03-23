from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Exchange(Base):
    __tablename__ = 'exchanges'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    arp_data = relationship("ARPData", back_populates="exchange")
    btc_price = relationship("BTCPrice", back_populates="exchange")

class ARPData(Base):
    __tablename__ = 'arp_data'
    
    id = Column(Integer, primary_key=True)
    exchange_id = Column(Integer, ForeignKey('exchanges.id'), nullable=False)
    coin = Column(String, nullable=False)
    arp_value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    exchange = relationship("Exchange", back_populates="arp_data")

class BTCPrice(Base):
    __tablename__ = 'btc_prices'
    
    id = Column(Integer, primary_key=True)
    exchange_id = Column(Integer, ForeignKey('exchanges.id'), nullable=False)
    price = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    exchange = relationship("Exchange", back_populates="btc_price")