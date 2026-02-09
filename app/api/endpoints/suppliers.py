from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.orm_models import Supplier
from app.models.schemas import SupplierCreate, SupplierResponse

# === 1. ROUTER STATT APP INITIALISIERUNG ===
router = APIRouter(
    prefix = "/api/suppliers",
    tags = ["Suppliers"]
)

# === 2. CRUD ENDPUNKT FÜR SUPPLIERS ===

# === 2.1 CREATE - NEUEN LIEFERANTEN ANLEGEN ===
@router.post("/", response_model=SupplierResponse)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    db_supplier = Supplier(
        name = supplier.name,
        delivery_reliability = supplier.delivery_reliability,
        avg_delivery_days = supplier.avg_delivery_days,
        price_level = supplier.price_level,
        quality_score = supplier.quality_score
    )
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

# === 2.2 READ ALL - ALLE LIEFERANTEN ANZEIGEN ===
@router.get("/", response_model=list[SupplierResponse])
def get_all_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()

# === 2.3 READ ONE - EINEN LIEFERANTEN NACH ID ABRUFEN ===
@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id : int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Lieferant nicht gefunden")
    return supplier                      