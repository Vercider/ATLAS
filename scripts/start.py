import subprocess
import time
import sys
import os
import requests

def wait_for_api(url="http://127.0.0.1:8000/api/inventory/", timeout=15):
    """Wartet bis die API erreichbar ist."""
    print("⏳ Warte auf API...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print("✅ API ist bereit!")
                return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    print("⚠️ API nicht erreichbar nach Timeout!")
    return False

def main():
    """Startet FastAPI und Streamlit gleichzeitig."""

    print("=" * 50)
    print("🛰️  A.T.L.A.S. wird gestartet...")
    print("=" * 50)

    # === 1. FastAPI starten ===
    print("\n🚀 Starte FastAPI auf Port 8000...")
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.api.main:app", "--port", "8000"],
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )

    # Warte bis API wirklich bereit ist
    api_ready = wait_for_api()

    if not api_ready:
        print("❌ API konnte nicht gestartet werden. Abbruch.")
        api_process.terminate()
        return

    # === 2. Streamlit starten ===
    print("📊 Starte Streamlit Dashboard auf Port 8501...")
    dashboard_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "app", "frontend", "dashboard.py"
    )
    streamlit_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", dashboard_path, "--server.port", "8501"],
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )

    print("\n" + "=" * 50)
    print("✅ A.T.L.A.S. läuft!")
    print("   API:       http://localhost:8000")
    print("   API Docs:  http://localhost:8000/docs")
    print("   Dashboard: http://localhost:8501")
    print("=" * 50)
    print("\n⛔ Zum Beenden: Strg + C drücken\n")

    # === 3. Warte auf Beenden ===
    try:
        api_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 A.T.L.A.S. wird beendet...")
        api_process.terminate()
        streamlit_process.terminate()
        api_process.wait()
        streamlit_process.wait()
        print("👋 Auf Wiedersehen!\n")

if __name__ == "__main__":
    main()

