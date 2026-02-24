from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.orm_models import Inventory, Supplier
from app.models.schemas import InventoryCreate, InventoryResponse
from scripts.seed_data import add_data

# === 1. ROUTER STATT APP INITIALISIERUNG ===
router = APIRouter(
    prefix="/api/inventory",
    tags=["Inventory"]
)

# === 2. CRUD ENDPUNKT FÜR INVENTORY ===

# === 2.1 CREATE - NEUES PRODUKT ANLEGEN ===
@router.post("/", response_model=InventoryResponse)
def create_inventory_item(item: InventoryCreate, db: Session = Depends(get_db)):
    db_item = Inventory(
        product_name = item.product_name,
        quantity = item.quantity,
        price = item.price,
        category = item.category
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# === 2.2 READ ALL - Alle Produkte aufrufen ===
@router.get("/", response_model=list[InventoryResponse])
def get_all_inventory(db:Session = Depends(get_db)):
    return db.query(Inventory).all()

# === 2.3 READ ONE - Ein Produkt nach ID abrufen ===
@router.get("/{item_id}", response_model = InventoryResponse)
def get_inventory_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden")
    return item

# === 2.4 EXTENDED SEED - Datenbank um 500 Produkte und 50 Lieferanten erhöht ===
@router.post("/seed")
def sedd_more_data(db: Session = Depends(get_db)):
    products_before = db.query(Inventory).count()
    suppliers_before = db.query(Supplier).count()

    result = add_data(db)

    products_after = db.query(Inventory).count()
    suppliers_after = db.query(Supplier).count()

    return {
        "Hinzugefügte Produkte": result["Produkte"],
        "Hinzugefügte Lieferanten": result["Lieferanten"],
        "Gesamt Produkte vorher": products_before,
        "Gesamt Produkte nachher": products_after,
        "Gesamt Lieferanten vorher": suppliers_before,
        "Gesamt Lieferanten nachher": suppliers_after
    }