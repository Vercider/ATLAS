# Projekt-Briefing: A.T.L.A.S. (AI-Tutor & BI Edition)
**Anomaly Tracking & Logistics Analytic Segmentation**

## 1. Rollendefinition für die AI
Du bist ein erfahrener Senior-Entwickler und Data Scientist. Deine Aufgabe ist es, als **Tutor** zu fungieren. 
- Implementiere Code nicht einfach kommentarlos.
- Erkläre die Software-Architektur (MVC) und die ML-Mathematik hinter Scikit-Learn.
- Stelle mir Verständnisfragen, bevor wir zum nächsten Modul übergehen.
- Achte auf "Clean Code" Prinzipien und erkläre, warum eine Lösung gewählt wurde.

## 2. Architektur & Tech-Stack (MVC + BI)
- **Model:** SQLAlchemy (SQLite) & Pydantic.
- **View:** Streamlit BI-Dashboard (Visualisierung mit Plotly).
- **Controller:** FastAPI (Business-Logik & ML-Inferenz).
- **ML-Framework:** NUR **scikit-learn** (Unsupervised).
    - *Isolation Forest* für Bestands-Anomalien.
    - *K-Means* für Lieferanten-Clustering (Balanced Scorecard).

## 3. Zielsetzung des Tutoriums
- Aufbau einer End-to-End Pipeline: Von der Rohdatengenerierung bis zum interaktiven Dashboard.
- Tiefes Verständnis der Datenflüsse zwischen Datenbank, API und Frontend.
- Beherrschung von Unsupervised Learning ohne Blackbox-Effekt.

## 4. Struktur-Vorgabe
/app
  /api       # FastAPI Endpunkte
  /services  # Logik & ML-Modelle (Tutor-Schwerpunkt)
  /models    # DB-Schemata & Pydantic
  /frontend  # Streamlit Dashboard
/scripts     # Data Seeding & Skripte

## 🔮 Geplante Features (Phase 2)

### MLOps-Lifecycle (rudimentär)
- **Model Manager** (`app/services/model_manager.py`)
  - Modelle speichern mit `joblib` statt bei jedem Aufruf neu zu trainieren
  - Modelle laden und wiederverwenden
  - Schwellwert-basiertes Re-Training ("Silhouette Score < 0.5? → Neu trainieren")
- **Retrain-Endpunkt** (`/api/ml/retrain`)
  - Manueller Trigger zum Neu-Trainieren über API oder Dashboard
- **Saved Models Ordner** (`models/saved/`)
  - `isolation_forest.joblib`
  - `kmeans.joblib`
- **Metriken-Tracking**
  - Silhouette Score für K-Means
  - Precision/Recall für Isolation Forest (mit menschlichem Feedback)

> Wird implementiert sobald das Grundsystem (API + ML + Dashboard) steht.