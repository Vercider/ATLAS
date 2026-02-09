from pydantic import BaseModel
from datetime import datetime

# === 1.INVENTORY SCHEMAS ===

# === 1.1 SCHEMA ANLAGE DES INVENTORY-EINTRAGS ===
class InventoryCreate(BaseModel):
    product_name: str
    quantity: int
    price: float
    category: str

# === 1.2 SCHEMA API-ANTWORT(INKL. ID + TIMESTAMP) ===
class InventoryResponse(BaseModel):
    id: int
    product_name: str
    quantity: int
    price: float
    category: str
    last_updated = datetime

    class Config:
        from_attributes = True

# === 2.SUPPLIER SCHMEAS ===

# === 2.1 SCHEMA ANLAGE DES SUPPLIERS-EINTRAGS ===
class SupplierCreate(BaseModel):
    name: str
    delivery_reliability: float
    avg_delivery_days: float
    price_level = float
    quality_score = float

# === 2.2 SCHEMA FÜR DIE API-ANTWORT ===
class SupplierResponse(BaseModel):
    id: int
    name: str
    delivery_reliability: float
    avg_delivery_days: float
    price_level: float
    quality_score:float

    class Config:
        from_attributes = True

