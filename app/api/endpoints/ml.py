from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.anomaly_detection import detect_anomalies
from app.services.clustering import cluster_suppliers
from app.services.model_manager import model_exists
from app.services.model_monitor import get_model_status, evaluate_models

import os

router = APIRouter(
    prefix = "/api/ml",
    tags = ["Machine Learning"]
)

# === 1. Router-Ping für Isolation Forest ===
@router.get("/anomalies")
def get_anomalies( db: Session = Depends(get_db)):
    """Führt Isolation Forest aus und gibt Anomalien zurück."""
    result = detect_anomalies(db)
    return result

# === 2. Router-Ping für Kmeans-Clustering ===
@router.get("/clusters")
def get_clusters(db: Session = Depends(get_db)):
    """Führt K-Means aus und gibt Clusters zurück."""
    result = cluster_suppliers(db)
    return result

# === 3. Router-Ping für Retrain - Modelle löschen und neu trianieren ===
@router.post("/retrain")
def retrain_models(db: Session = Depends(get_db)):
    """Löscht gespeicherte Modelle und trainiert neu."""
    from app.services.model_manager import MODEL_DIR

    # Alte Modelle löschen
    for filename in os.listdir(MODEL_DIR):
        if filename.endswith(".joblib"):
            os.remove(os.path.join(MODEL_DIR, filename))

    # Neu trainieren durch Aufruf
    anomaly_result = detect_anomalies(db)
    cluster_result = cluster_suppliers(db)

    return {
        "message": "Modelle erfolgreich neu trainiert!",
        "anomalien_gefunden": anomaly_result["total_anomalies"],
        "cluster_erstellt": cluster_result["n_clusters"]
    }

# === 4. Router-Ping für Statusabruf des Modell-Status ===
@router.get("/status")
def get_status():
    """Gibt den Status beider Modelle zurück."""
    return get_model_status()

# === 5. Router-Ping für Modellevaluierung ===
@router.post("/evaluate")
def evaluate(db: Session = Depends(get_db)):
    """Evaluiert beide Modelle und spiechert Ergebnisse im Log."""
    return evaluate_models(db) 