import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sqlalchemy.orm import Session

from app.models.orm_models import Supplier

FEATURE_COLUMNS = ["delivery_reliability", "avg_delivery_days", "price_level", "quality_score"]
N_CLUSTERS = 3
RANDOM_STATE = 42

def get_supplier_dataframe(db: Session) -> pd.DataFrame:
    """Lädt alle Supplier-Daten aus der DB in einen Pandas Dataframe"""
    suppliers = db.query(Supplier).all()

    data = [{
        "id": supplier.id,
        "name": supplier.name,
        "delivery_reliability": supplier.delivery_reliability,
        "avg_delivery_days": supplier.avg_delivery_days,
        "price_level": supplier.price_level,
        "quality_score": supplier.quality_score
    } for supplier in suppliers]

    return pd.DataFrame(data)

def cluster_suppliers(db: Session) -> dict:
    """Führt K-Means Clustering auf den Supplier-Daten aus."""

    # === 1. Daten laden ===
    df = get_supplier_dataframe(db)

    if df.empty:
        return {"error": "Keine Daten vorhanden"}
    
    # === 2. Features extrahieren und skalieren ===
    features = df[FEATURE_COLUMNS]
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # === 3. Modell erstellen und trainieren ===
    model = KMeans(
        n_clusters = N_CLUSTERS,
        random_state = RANDOM_STATE,
        n_init = 10
    )
    model.fit(features_scaled)

    # === 4. CLuster-Labels zuweisen ===
    df["cluster"] = model.predict(features_scaled)

    # === 5. Cluster-Statistiken berechnen ===
    cluster_stats = {}
    for cluster_id in range(N_CLUSTERS):
        cluster_data = df[df["cluster"] == cluster_id]
        cluster_features = cluster_data[FEATURE_COLUMNS]

        cluster_stats[int(cluster_id)] = {
            "count": len(cluster_data),
            "members": cluster_data[["id", "name", "cluster"]].to_dict(orient="records"),
            "avg_values": {
                col: round(cluster_features[col].mean(), 3)
                for col in FEATURE_COLUMNS
            }
        }

    # === 6. Ergebnisse zurückgeben ===
    return {
        "total_suppliers": len(df),
        "n_clusters": N_CLUSTERS,
        "cluster_stats": cluster_stats,
        "all_suppliers": df.to_dict(orient="records"),
        "model_params": {
            "n_clusters": N_CLUSTERS,
            "features_used": FEATURE_COLUMNS,
            "n_init": 10
        }
    }



