import streamlit as st
import requests
import pandas as pd

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
    ["Dashboard", "Anomalierkennung", "Lieferanten-Cluster"]
)

# === Seiten-Logik ===
if page == "Dashboard":
    st.header("📊 Übersicht")
    st.write("Hier kommt die Übersicht hin")

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

elif page == "Anomalierkennung":
    st.header("🔍 Anomalieerkennung")
    st.write("Hier kommt der Isolation Forest hin")

elif page == "Lieferanten-Cluster":
    st.header("🏷️ Lieferanten-Cluster")
    st.write("Hier kommt K-Means hin.")