import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import base64
import os

# === Konfiguration ===
API_BASE_URL = "http://localhost:8000"

# == Seiten-Setup ===
st.set_page_config(
    page_title = "A.T.L.A.S.",
    page_icon = "🛰️",
    layout = "wide"
)

# === Hintergrundbild ===
def set_background(image_path):
    """Lädt ein Bild und setzt es als Hintergrund via CSS."""
    with open(image_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()

    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_data}");
            background-size: 65%;
            background-position: top center;
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-color: #0e1117;
        }}
        .stApp > header {{
            background-color: transparent;
        }}
        .block-container {{
            background-color: rgba(14, 17, 23, 0.88);
            border-radius: 10px;
            padding: 2rem;
        }}
        [data-testid="stSidebar"] {{
            background-color: rgba(14, 17, 23, 0.95);
        }}
        </style>
    """, unsafe_allow_html=True)

bg_path = os.path.join(os.path.dirname(__file__), "assets", "atlas_bg.png")
if os.path.exists(bg_path):
    set_background(bg_path)

# === Sidebar Navigation ===
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Bereich wählen:",
    ["Dashboard", "Anomalieerkennung", "Lieferanten-Cluster", "MLOps Monitoring"]
)

# === Seiten-Logik ===
if page == "Dashboard":
    st.header("📊 Übersicht")

    try:
        inventory_response = requests.get(f"{API_BASE_URL}/api/inventory/")
        inventory_data = inventory_response.json()
    except requests.exceptions.ConnectionError:
        st.error("⚠️ API nicht erreichbar! Bitte zuerst FastAPI starten.")
        st.stop()

    supplier_response = requests.get(f"{API_BASE_URL}/api/suppliers/")

    supplier_data = supplier_response.json()

    # Drei Kennzahlen nebeneinander
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📦 Produkte im Lager", len(inventory_data))
    with col2:
        st.metric("🚚 Lieferanten", len(supplier_data))
    with col3:
        kategorien = len(set(item["category"] for item in inventory_data))
        st.metric("🏷️ Kategorien", kategorien)

    # == Datenbank erweitern ===
    st.divider()
    st.subheader("🗃️ Datenbank erweitern")

    if st.button("➕ 500 Produkte & 50 Lieferanten hinzufügen"):
        response = requests.post(f"{API_BASE_URL}/api/inventory/seed")
        result = response.json()

        st.success(
            f"✅ Erfolgreich hinzugefügt: "
            f"{result['Hinzugefügte Produkte']} Produkte, "
            f"{result['Hinzugefügte Lieferanten']} Lieferanten"
        )

        col_before, col_after = st.columns(2)
        with col_before:
            st.metric("📦 Produkte vorher", result["Produkte vorher"])
            st.metric("🚚 Lieferanten vorher", result["Lieferanten vorher"])
        with col_after:
            st.metric("📦 Produkte nachher", result["Produkte nachher"])
            st.metric("🚚 Lieferanten nachher", result["Lieferanten nachher"])

elif page == "Anomalieerkennung":
    st.header("🔍 Anomalieerkennung")
    
    # ML-Ergebnisse von der API laden
    response = requests.get(f"{API_BASE_URL}/api/ml/anomalies")
    result = response.json()

    # Kennzahlen oben anzeigen
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📦 Geprüfte Produkte", result["total_items"])
    with col2:
        st.metric("⚠️ Anomalien gefunden", result["total_anomalies"])
    with col3:
        st.metric("📊 Anomalie-Anteil", f"{result['anomaly_percentage']}%")

    # Trennlinie
    st.divider()

    # Scatter-Plot: Alle Produkte visualisieren
    st.subheader("Scatter-Plot: Quantity vs. Price")

    # Alle Daten nochmal von der API holen für den Plot
    inv_response = requests.get(f"{API_BASE_URL}/api/inventory/")
    inv_data = inv_response.json()
    df = pd.DataFrame(inv_data)

    # Anomalie-IDs sammeln
    anomaly_ids = [item["id"] for item in result["anomalies"]]

    # Neue Spalte: Ist es eine Anomalie?
    df["Status"] = df["id"].apply(
        lambda x: "⚠️ Anomalie" if x in anomaly_ids else "✅ Normal"
    )

    # Plotly Scatter-Chart
    fig = px.scatter(
        df,
        x = "quantity",
        y = "price",
        color = "Status",
        hover_data = ["product_name", "category"],
        color_discrete_map = {
            "✅ Normal": "#2ecc71",
            "⚠️ Anomalie": "#e74c3c"
        },
        title = "Produkte: Menge vs. Preis"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Anomalie-Tabelle
    st.subheader("⚠️ Erkannte Anomalien")
    if result["anomalies"]:
        anomaly_df = pd.DataFrame(result["anomalies"])
        st.dataframe(anomaly_df, use_container_width=True)
    else:
        st.info("Keine Anomalien gefunden.")

elif page == "Lieferanten-Cluster":
    st.header("🏷️ Lieferanten-Cluster")
    
    # ML-Ergebnisse von der API laden
    response = requests.get(f"{API_BASE_URL}/api/ml/clusters")
    result = response.json()

    # Kennzahlen oben
    col1, col2 = st.columns(2)

    with col1:
        st.metric("🚚 Lieferanten gesamt", result["total_suppliers"])
    with col2:
        st.metric("🏷️ Cluster gefunden", result["n_clusters"])

    # Trennlinie
    st.divider()

    # Cluster-Statistiken anzeigen
    st.subheader("Cluster-Übersicht")

    cluster_names = {0: "⭐ Premium", 1: "📦 Standard", 2: "⚠️ Risiko"}

    for cluster_id, stats in result["cluster_stats"].items():
        cluster_name = cluster_names.get(int(cluster_id), f"Cluster {cluster_id}")

        with st.expander(f"{cluster_name} - {stats['count']} Lieferanten"):
            # Durchschnittswerte anzeigen
            avg = stats["avg_values"]

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Zuverlässigkeit", f"{avg['delivery_reliability']:.1%}")
            with col2:
                st.metric("Ø Liefertage", f"{avg['avg_delivery_days']:.1f}")
            with col3:
                st.metric("Preisniveau", f"{avg['price_level']:.1%}")
            with col4:
                st.metric("Qualität", f"{avg['quality_score']:.1%}")

            # Mitglieder als Tabelle
            if stats["members"]:
                members_df = pd.DataFrame(stats["members"])
                st.dataframe(members_df, use_container_width=True)
    
    # Trennlinie
    st.divider()

    # Zwei Scatter-Plots nebeneinander
    st.subheader("Scatter-Plots: Lieferanten-Analyse")

    all_suppliers = pd.DataFrame(result["all_suppliers"])
    all_suppliers["Cluster"] = all_suppliers["cluster"].map(cluster_names)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        fig1 = px.scatter(
            all_suppliers,
            x="avg_delivery_days",
            y="delivery_reliability",
            color="Cluster",
            hover_data=["name"],
            color_discrete_map={
                "⭐ Premium": "#2ecc71",
                "📦 Standard": "#3498db",
                "⚠️ Risiko": "#e74c3c"
            },
            title="Liefertage vs. Zuverlässigkeit"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with chart_col2:
        fig2 = px.scatter(
            all_suppliers,
            x="price_level",
            y="quality_score",
            color="Cluster",
            hover_data=["name"],
            color_discrete_map={
                "⭐ Premium": "#2ecc71",
                "📦 Standard": "#3498db",
                "⚠️ Risiko": "#e74c3c"
            },
            title="Preisniveau vs. Qualität"
        )
        st.plotly_chart(fig2, use_container_width=True)

elif page == "MLOps Monitoring":
    st.header("🔬 MLOps Monitoring")


    # === Modell-Status laden ===
    try:
        status_response = requests.get(f"{API_BASE_URL}/api/ml/status")
        status_data = status_response.json()
    except requests.exceptions.ConnectionError:
        st.error("⚠️ API nicht erreichbar!")
        st.stop()

    # === Status beider Modelle anzeigen ===
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Isolation Forest")
        if "status" in status_data["isolation_forest"]:
            st.warning("Nicht trainiert")
        else:
            meta = status_data["isolation_forest"]
            st.success("Trainiert ✅")
            st.write(f"📅 Gespeichert am: {meta['gespeichert_am'][:10]}")
            st.write(f"📊 Datenpunkte: {meta['anzahl_datenpunkte']}")
    
    with col2:
        st.subheader("📦 K-Means Clustering")
        if "status" in status_data["kmeans_clustering"]:
            st.warning("Nicht trainiert")
        else:
            meta = status_data["kmeans_clustering"]
            st.success("Trainiert ✅")
            st.write(f"📅 Gespeichert am: {meta['gespeichert_am'][:10]}")
            st.write(f"📊 Lieferanten: {meta['anzahl_lieferanten']}")

    # === Retrain Button ===
    st.divider()
    st.subheader("🔄 Modelle neu trainieren")

    if st.button("🔄 Retrain starten"):
        retrain_response = requests.post(f"{API_BASE_URL}/api/ml/retrain")
        result = retrain_response.json()

        st.success(f"✅ {result['message']}")
        st.write(f"🔍 Anomalien gefunden: {result['anomalien_gefunden']}")
        st.write(f"📦 Cluster erstellt: {result['cluster_erstellt']}")

    # === Evaluate Button ===
    st.divider()
    st.subheader("📊 Modelle evaluieren")

    if st.button("📊 Evaluation starten"):
        eval_response = requests.post(f"{API_BASE_URL}/api/ml/evaluate")
        result = eval_response.json()

        st.success("✅ Evaluation abgeschlossen!")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("📦 Produkte geprüft", result["anomaly_detection"]["total_products"])
            st.metric("🔍 Anomalien gefunden", result["anomaly_detection"]["anomalies_found"])
            st.metric("📈 Anomalie-Rate", f"{result['anomaly_detection']['anomaly_ratio'] * 100:.1f}")
        with col_b:
            st.metric("🚚 Lieferanten geprüft", result["clustering"]["total_suppliers"])
            st.metric("📦 Cluster", result["clustering"]["n_clusters"])