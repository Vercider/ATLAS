import streamlit as st

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

elif page == "Anomalierkennung":
    st.header("🔍 Anomalieerkennung")
    st.write("Hier kommt der Isolation Forest hin")

elif page == "Lieferanten-Cluster":
    st.header("🏷️ Lieferanten-Cluster")
    st.write("Hier kommt K-Means hin.")