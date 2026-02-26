import json
import os
from datetime import datetime

from sqlalchemy.orm import Session

from app.services.anomaly_detection import detect_anomalies
from app.services.clustering import cluster_suppliers
from app.services.model_manager import load_metadata

# === 1. Pfad zur Monitoring-Log Datei ===
MONITOR_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "ml_models")
MONITOR_LOG = os.path.join(MONITOR_DIR, "monitor_log.json")

# === 2. Modell-Status abrufen ===
def get_model_status():
    """Gibt den aktuellen Status beider Modelle zurück."""

    anomaly_meta = load_metadata("isolation_forest")
    cluster_meta = load_metadata("kmeans_clustering")

    return {
        "isolation_forest": anomaly_meta if anomaly_meta else {"status": "Nicht trainiert"},
        "kmeans_clustering": cluster_meta if cluster_meta else {"status": "Nicht trainiert"}
    }