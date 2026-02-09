from fastapi import FastAPI
from app.models.database import engine, Base
from app.api.endpoints.inventory import router as inventory_router

# === 1.TABELLEN ERSCHAFFEN (FALLS NICHT VORHANDEN) ===
Base.metadata.create_all(bind=engine)

# === 2.FAST-API-INSTANZ ===
app = FastAPI(
    title="A.T.L.A.S",
    description="Anomaliy Tracking & Logistics Analytical Segmentation",
    version="0.1.0"
)

# === 3.INVENTORY-ROUTER EINBINDUNG ===
app.include_router(inventory_router)

# === 4.TEST-ENDPUNKT ===
@app.get("/")
def read_root():
    return {"status": "online", "projekt": "ATLAS"}