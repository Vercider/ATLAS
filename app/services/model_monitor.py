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

# === 3. Log-Eintrag speichern (intern) ===
def _save_log_entry(entry):
    """Speichert einen Eintrag in die Monitor-Log Datei."""

    os.makedirs(MONITOR_DIR, exist_ok = True)

    # Bestehende Logs laden oder leere Liste
    if os.path.exists(MONITOR_LOG):
        with open(MONITOR_LOG, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    # Neuen Eintrag hinzufügen
    logs.append(entry)

    # Zurückschreiben
    with open(MONITOR_LOG, "w") as f:
        json.dump(logs, f, indent = 4)

# === 4. Modelle evaluieren ===
def evaluate_models(db:Session):
    """Führt beide Modelle aus und speichert die Ergebnisse im Log"""

    timestamp = datetime.now().isoformat()

    # Anomalie-Ergebnisse holen
    anomaly_result = detect_anomalies(db)
    total_products = anomaly_result["total_items"]
    anomalies_found = anomaly_result["total_anomalies"]
    anomaly_ratio = anomalies_found / total_products if total_products > 0 else 0

    # Cluster-Ergebnisse holen
    cluster_result = cluster_suppliers(db)
    total_suppliers = cluster_result["total_suppliers"]

    # Log-Eintrag erstellen
    log_entry = {
        "timestamp": timestamp,
        "anomaly_detection": {
            "total_products": total_products,
            "anomalies_found": anomalies_found,
            "anomaly_ratio": round(anomaly_ratio, 4)
        },
        "clustering": {
            "total_suppliers": total_suppliers,
            "n_clusters": cluster_result["n_clusters"]
        }
    }

    # Log speichern
    _save_log_entry(log_entry)

    return log_entry