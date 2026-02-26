import joblib
import os
import json
from datetime import datetime

# === 1.Pfad zum Modell-Ordner ===
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "ml_models")

# === 2.Modell speichern ===
def save_model(model, model_name, metadata = None):
    """Speicher ein ML-Modell und seine Metadaten"""

    # Ordner erstellen falls nicht vorhanden
    os.makedirs(MODEL_DIR, exist_ok = True)

    # Modell speichern
    model_path = os.path.join(MODEL_DIR, f"{model_name}.joblib")
    joblib.dump(model, model_path)

    # Metadaten speichern
    meta = {
        "model_name": model_name,
        "gespeichert_am": datetime.now().isoformat(),
        "model_pfad": model_path,
    }

    # Zusätzliche Metadaten hinzufügen falls vorhanden
    if metadata:
        meta.update(metadata)

    meta_path = os.path.join(MODEL_DIR, f"{model_name}_meta.json")
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent = 4)

    return model_path

# === 3.Modell laden ===
def load_model(model_name):
    """Lädt ein gespeichertes ML-Modell. Gibt None zurück falls nicht vorhanden."""

    model_path = os.path.join(MODEL_DIR, f"{model_name}.joblib")

    if not os.path.exists(model_path):
        return None
    
    return joblib.load(model_path)

# === 4. Metadaten laden ===
def load_metadata(model_name):
    """Lädt die Metadaten eines gespeicherten Modells. Gibt None zurück falls nicht vorhanden."""

    meta_path = os.path.join(MODEL_DIR, f"{model_name}_meta.json")

    if not os.path.exists(meta_path):
        return None
    
    with open(meta_path, "r") as f:
        return json.load(f)