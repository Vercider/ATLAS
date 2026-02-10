import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# === Konfiguration ===
API_BASE_URL = "http://localhost:8000"

# == Seiten-Setup ===
st.set_page_config(
    page_title = "A.T.L.A.S.",
    page_icon = "🛰️",
    layout = "wide"
)

# === Titel ===
st.title("🛰️ A.T.L.A.S.")
st.markdown("**Anomaly Tracking & Logistics Analytic Segmentation**")

# === Sidebar Navigation ===
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Bereich wählen:",
    ["Dashboard", "Anomalieerkennung", "Lieferanten-Cluster"]
)

# === Seiten-Logik ===
if page == "Dashboard":
    st.header("📊 Übersicht")
    
    # Daten von der API laden
    inventory_response = requests.get(f"{API_BASE_URL}/api/inventory/")
    supplier_response = requests.get(f"{API_BASE_URL}/api/suppliers/")

    inventory_data = inventory_response.json()
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