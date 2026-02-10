import pandas as pd
from sklearn.ensemble import IsolationForest
from sqlalchemy.orm import Session

from app.models.orm_models import Inventory

FEATURE_COLUMNS = ["quantity", "price"]
CONTAMINATION = 0.05
RANDOM_STATE = 42

def get_inventory_dataframe(db: Session) -> pd.DataFrame:
    """Lädt alle Inventory-Daten aus der DB in einen Pandas Dataframe"""
    items = db.query(Inventory).all()

    data = [{
        "id" : item.id,
        "product_name" : item.product_name,
        "quantity" : item.quantity,
        "price" : item.price,
        "category" : item.category 
    } for item in items]

    return pd.DataFrame(data)

def detect_anomalies(db: Session) -> dict:
    """Führt Isolation Forest auf den Inventory-Daten aus."""

    # === 1. Daten laden ===
    df = get_inventory_dataframe(db)

    if df.empty:
        return {"error": "Keine Daten vorhanden"}
    
    # === 2. Features extrahieren ===
    features = df[FEATURE_COLUMNS]

    # === 3. Modell erstellen und trainieren ===
    model = IsolationForest(
        contamination = CONTAMINATION,
        random_state = RANDOM_STATE,
        n_estimators = 100
    )

    model.fit(features)

    # === 4. Vorhersage treffen ===
    df["anomaly_score"] = model.decision_function(features)
    df["is_anomaly"] = model.predict(features)

    # === 5. Ergebnisse aufbereiten ===
    anomalies = df[df["is_anomaly"] == -1 ].to_dict(orient = "records")
    normal = df[df["is_anomaly"] == 1 ].to_dict(orient = "records")

    return {
        "total_items": len(df),
        "total_anomalies": len(anomalies),
        "anomaly_percentage": round(len(anomalies) / len(df) * 100, 2),
        "anomalies": anomalies,
        "normal_items": len(normal),
        "model_params": {
            "contamination": CONTAMINATION,
            "features_used": FEATURE_COLUMNS,
            "n_estimators": 100
        }
    } 