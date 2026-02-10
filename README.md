<div align="center">

# 🛰️ A.T.L.A.S.

### Anomaly Tracking & Logistics Analytic Segmentation

*ML-gestütztes Supply-Chain-Management-System mit Anomalieerkennung und Lieferanten-Clustering*

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-009688?logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8-F7931E?logo=scikit-learn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54-FF4B4B?logo=streamlit&logoColor=white)

</div>

---

## 📋 Über das Projekt

ATLAS ist ein Supply-Chain-Management-System das mithilfe von Machine Learning automatisch **ungewöhnliche Lagerbestände erkennt** und **Lieferanten nach Leistungsprofil gruppiert**.

Das System nutzt zwei ML-Modelle:
- **Isolation Forest** — Erkennt Anomalien in Lagerdaten (z.B. unrealistische Mengen oder Preise)
- **K-Means Clustering** — Gruppiert Lieferanten in Premium, Standard und Risiko-Kategorien

## 🖥️ Screenshots

### Dashboard — Übersicht
> Zentrale Kennzahlen auf einen Blick: Produkte, Lieferanten, Kategorien

### Anomalieerkennung
> Scatter-Plot visualisiert normale Produkte (grün) und erkannte Anomalien (rot)

### Lieferanten-Cluster
> Zwei Scatter-Plots zeigen die Cluster-Trennung über alle 4 Features

---

## 🏗️ Architektur

```
┌─────────────────┐     HTTP      ┌─────────────────┐     SQL      ┌──────────┐
│    Streamlit     │ ──────────→  │     FastAPI      │ ──────────→  │  SQLite  │
│    Dashboard     │ ←──────────  │   REST API       │ ←──────────  │    DB    │
│    (Port 8501)   │    JSON      │   (Port 8000)    │   Data       │          │
└─────────────────┘               └────────┬─────────┘              └──────────┘
                                           │
                                    ┌──────▼──────┐
                                    │  ML Services │
                                    ├─────────────┤
                                    │ Isolation    │
                                    │ Forest       │
                                    ├─────────────┤
                                    │ K-Means      │
                                    │ Clustering   │
                                    └─────────────┘
```

**Architekturmuster:** MVC (Model-View-Controller)

| Schicht | Technologie | Aufgabe |
|---|---|---|
| **View** | Streamlit + Plotly | Dashboard, Charts, Tabellen |
| **Controller** | FastAPI | REST API, Routing, Validierung |
| **Model** | SQLAlchemy + SQLite | Datenbankzugriff, ORM |
| **Services** | scikit-learn + Pandas | ML-Modelle, Datenverarbeitung |

---

## 🚀 Schnellstart

### Voraussetzungen
- Python 3.11 oder höher
- pip (Python Package Manager)

### Installation

```bash
# Repository klonen
git clone https://github.com/DEIN-USERNAME/ATLAS.git
cd ATLAS

# Virtuelle Umgebung erstellen
python -m venv venv

# Aktivieren (Windows)
venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt
```

### Datenbank befüllen

```bash
py scripts/seed_data.py
```
> Erstellt 500 Produkte, 50 Lieferanten und 5% bewusste Anomalien

### Starten

```bash
py scripts/start.py
```

| Service | URL |
|---|---|
| Dashboard | http://localhost:8501 |
| API Docs | http://localhost:8000/docs |
| API | http://localhost:8000 |

> Zum Beenden: `Strg + C` im Terminal

---

## 📡 API-Endpunkte

| Methode | Route | Beschreibung |
|---|---|---|
| `GET` | `/api/inventory/` | Alle Produkte abrufen |
| `POST` | `/api/inventory/` | Neues Produkt anlegen |
| `GET` | `/api/inventory/{id}` | Einzelnes Produkt abrufen |
| `GET` | `/api/suppliers/` | Alle Lieferanten abrufen |
| `POST` | `/api/suppliers/` | Neuen Lieferanten anlegen |
| `GET` | `/api/suppliers/{id}` | Einzelnen Lieferanten abrufen |
| `GET` | `/api/ml/anomalies` | Anomalieerkennung ausführen |
| `GET` | `/api/ml/clusters` | Lieferanten-Clustering ausführen |

> Interaktive API-Dokumentation: http://localhost:8000/docs

---

## 🤖 ML-Modelle

### Isolation Forest — Anomalieerkennung

| Parameter | Wert |
|---|---|
| Features | `quantity`, `price`, `reorder_level` |
| Contamination | 5% |
| Methode | Unsupervised Learning |

Erkennt Produkte mit ungewöhnlichen Kombinationen aus Menge, Preis und Mindestbestand.

### K-Means Clustering — Lieferantenbewertung

| Parameter | Wert |
|---|---|
| Features | `delivery_reliability`, `avg_delivery_days`, `price_level`, `quality_score` |
| Cluster | 3 (Premium, Standard, Risiko) |
| Methode | Unsupervised Learning |

Gruppiert Lieferanten automatisch nach Leistungsprofil.

---

## 📁 Projektstruktur

```
ATLAS/
├── app/
│   ├── api/
│   │   ├── main.py                  # FastAPI App + Router
│   │   ├── dependencies.py          # Session-Verwaltung
│   │   └── endpoints/
│   │       ├── inventory.py         # CRUD Inventory
│   │       ├── suppliers.py         # CRUD Suppliers
│   │       └── ml.py               # ML-Endpunkte
│   ├── models/
│   │   ├── database.py              # DB-Verbindung
│   │   ├── orm_models.py            # Tabellenstruktur
│   │   └── schemas.py              # Pydantic-Schemas
│   ├── services/
│   │   ├── anomaly_detection.py     # Isolation Forest
│   │   └── clustering.py           # K-Means
│   └── frontend/
│       ├── dashboard.py            # Streamlit Dashboard
│       └── assets/
│           └── atlas_bg.png        # Hintergrundbild
├── scripts/
│   ├── seed_data.py                # Testdaten-Generator
│   └── start.py                    # Ein-Klick-Start
├── atlas.md                        # Technische Dokumentation
├── requirements.txt                # Dependencies
└── README.md                       # Diese Datei
```

---

## 🗺️ Roadmap

- [x] FastAPI Backend mit CRUD-Endpunkten
- [x] Isolation Forest Anomalieerkennung
- [x] K-Means Lieferanten-Clustering
- [x] Streamlit Dashboard mit Plotly-Charts
- [x] Ein-Klick-Startskript
- [ ] MLOps-Lifecycle (Model Monitoring, Re-Training)
- [ ] Docker Deployment
- [ ] PostgreSQL statt SQLite
- [ ] Unit Tests + Integration Tests

---

## 🛠️ Tech Stack

| Paket | Version | Zweck |
|---|---|---|
| FastAPI | 0.128 | REST API Backend |
| SQLAlchemy | 2.0 | ORM + Datenbankzugriff |
| scikit-learn | 1.8 | Machine Learning |
| Pandas | 2.3 | Datenverarbeitung |
| Streamlit | 1.54 | Frontend Dashboard |
| Plotly | 6.5 | Interaktive Charts |
| Pydantic | 2.12 | Datenvalidierung |
| Uvicorn | 0.40 | ASGI Server |

---

<div align="center">

**Erstellt als ML-Engineering Projekt**

🛰️ *A.T.L.A.S. — Anomaly Tracking & Logistics Analytic Segmentation*

</div>