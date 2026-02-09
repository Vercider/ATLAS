from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

# === 1.TABELLE: LAGERBESTAND ===
class Inventory(Base):
    __tablename__ = "Lagerbestand"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    last_updated= Column(DateTime, server_default=func.now())

# === 2.TABELLE: LIEFERANTEN ===
class Supplier(Base):
    __tablename__ = "Lieferanten"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    delivery_reliability = Column(Float, nullable=False)
    avg_delivery_days = Column(Float, nullable=False)
    price_level = Column(Float, nullable=False)
    quality_score = Column(Float, nullable=False)
    