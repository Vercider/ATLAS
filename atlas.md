# 🛰️ A.T.L.A.S.
## Anomaly Tracking & Logistics Analytic Segmentation

### Projektbeschreibung
Supply-Chain-Management-System mit ML-gestützter Anomalieerkennung
und Lieferanten-Clustering. Das System erkennt automatisch ungewöhnliche
Lagerbestände (Isolation Forest) und gruppiert Lieferanten nach
Leistungsprofil (K-Means Clustering).

### Technologie-Stack
| Kategorie | Technologie |
|---|---|
| **Backend** | FastAPI + SQLAlchemy + SQLite |
| **ML** | scikit-learn (Isolation Forest, K-Means) |
| **Frontend** | Streamlit + Plotly |
| **Architektur** | MVC Pattern |
| **Sprache** | Python 3.11+ |

### Architektur (MVC)
```
View (Streamlit)  →  Controller (FastAPI)  →  Model/Service (DB + ML)
  dashboard.py        endpoints/*.py           orm_models.py
  Nur anzeigen        Vermittelt               anomaly_detection.py
  Port 8501           Port 8000                clustering.py
```

### Projektstruktur
```
ATLAS/
├── app/
│   ├── api/
│   │   ├── main.py                  FastAPI App + Router
│   │   ├── dependencies.py          Session-Verwaltung (DI)
│   │   └── endpoints/
│   │       ├── inventory.py         Inventory CRUD Endpunkte
│   │       ├── suppliers.py         Supplier CRUD Endpunkte
│   │       └── ml.py               ML-Ergebnis Endpunkte
│   ├── models/
│   │   ├── database.py              SQLite + SQLAlchemy Engine
│   │   ├── orm_models.py            Inventory + Supplier Tabellen
│   │   └── schemas.py              Pydantic Validierung
│   ├── services/
│   │   ├── anomaly_detection.py     Isolation Forest Service
│   │   └── clustering.py           K-Means Clustering Service
│   └── frontend/
│       ├── dashboard.py            Streamlit Dashboard
│       └── assets/
│           └── atlas_bg.png        Hintergrundbild
├── scripts/
│   ├── seed_data.py                Testdaten-Generator
│   └── start.py                    Ein-Klick-Startskript
├── atlas.md                        Projektdokumentation
└── requirements.txt                Python-Dependencies
```

### API-Endpunkte
| Methode | Route | Beschreibung |
|---|---|---|
| GET | `/api/inventory/` | Alle Produkte abrufen |
| POST | `/api/inventory/` | Neues Produkt anlegen |
| GET | `/api/inventory/{id}` | Einzelnes Produkt abrufen |
| GET | `/api/suppliers/` | Alle Lieferanten abrufen |
| POST | `/api/suppliers/` | Neuen Lieferanten anlegen |
| GET | `/api/suppliers/{id}` | Einzelnen Lieferanten abrufen |
| GET | `/api/ml/anomalies` | Isolation Forest ausführen |
| GET | `/api/ml/clusters` | K-Means Clustering ausführen |

### ML-Modelle

#### Isolation Forest (Anomalieerkennung)
- **Zweck:** Erkennt ungewöhnliche Lagerbestände
- **Features:** `quantity`, `price`, `reorder_level`
- **Methode:** Unsupervised Learning — findet Ausreißer ohne Labels
- **Konfiguration:** contamination=0.05, random_state=42
- **Ergebnis:** ~5% der Produkte als Anomalien markiert

#### K-Means Clustering (Lieferantenbewertung)
- **Zweck:** Gruppiert Lieferanten nach Leistungsprofil
- **Features:** `delivery_reliability`, `avg_delivery_days`, `price_level`, `quality_score`
- **Methode:** Unsupervised Learning — findet natürliche Gruppen
- **Konfiguration:** n_clusters=3, n_init=10, random_state=42
- **Ergebnis:** 3 Cluster (Premium, Standard, Risiko)

### Testdaten
- **500 Produkte** in 5 Kategorien (Befestigung, Elektronik, Werkzeug, Hydraulik, Verpackung)
- **50 Lieferanten** mit realistischen Leistungsdaten
- **5% bewusste Anomalien** (extreme Mengen/Preise) zum Testen

### Dashboard-Seiten
| Seite | Inhalt |
|---|---|
| **Dashboard** | Übersicht: Anzahl Produkte, Lieferanten, Kategorien |
| **Anomalieerkennung** | Scatter-Plot (Quantity vs. Price), Anomalie-Tabelle |
| **Lieferanten-Cluster** | Cluster-Expander mit Statistiken, zwei Scatter-Plots |

### Schnellstart
```bash
# 1. Repository klonen und venv erstellen
cd ATLAS
python -m venv venv
venv\Scripts\activate

# 2. Dependencies installieren
pip install -r requirements.txt

# 3. Datenbank befüllen
py scripts/seed_data.py

# 4. Alles starten
py scripts/start.py

# 5. Im Browser öffnen
# Dashboard: http://localhost:8501
# API Docs:  http://localhost:8000/docs
```

### Geplante Features (Phase 2)
- [ ] **MLOps-Lifecycle**
  - Modelle speichern/laden mit joblib
  - Model Monitoring (Silhouette Score, Precision/Recall)
  - Schwellwert-basiertes Re-Training
  - API-Endpunkt: `/api/ml/retrain`
  - Zentrale Modellverwaltung (`model_manager.py`)
- [ ] **Docker Deployment**
  - Dockerfile + docker-compose.yml
  - SQLite → PostgreSQL Migration
  - Umgebungsvariablen für Konfiguration
- [ ] **Erweiterte ML-Features**
  - Feature Engineering (z.B. Kapitalbindung = quantity × price)
  - Business Rules + ML kombiniert
  - Automatische Cluster-Benennung
- [ ] **Testing**
  - Unit Tests für Services
  - Integration Tests für API-Endpunkte
  - ML-Model Validierung