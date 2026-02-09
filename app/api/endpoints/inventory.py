from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.orm_models import Inventory
from app.models.schemas import InventoryCreate, InventoryResponse

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