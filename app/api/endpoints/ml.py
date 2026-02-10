from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.anomaly_detection import detect_anomalies
from app.services.clustering import cluster_suppliers

router = APIRouter(
    prefix = "/api/ml",
    tags = ["Machine Learning"]
)

@router.get("/anomalies")
def get_anomalies( db: Session = Depends(get_db)):
    """Führt Isolation Forest aus und gibt Anomalien zurück."""
    result = detect_anomalies(db)
    return result

@router.get("/clusters")
def get_clusters(db: Session = Depends(get_db)):
    """Führt K-Means aus und gibt Clusters zurück."""
    result = cluster_suppliers(db)
    return result