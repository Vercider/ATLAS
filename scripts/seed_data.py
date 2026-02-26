import sys
import os
import random
from datetime import datetime, timedelta

# === 1.Projektpfad hinzugefügen für Imports ===
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.database import SessionLocal, engine, Base
from app.models.orm_models import Inventory, Supplier

# === 2.Tabelle erstellen falls nötig ===
Base.metadata.create_all(bind=engine)

# === 3.Konfiguration ===
ANZAHL_PRODUKTE = 500
ANZAHL_LIEFERANTEN = 50
ANTEIL_ANOMALIEN = 0.05

# === 4.Kategorien und Produktnamen ===
KATEGORIEN = {
    "Befestigung": ["Schraube M4", "Schraube M8", "Mutter M6", "Bolzen M10", "Nagel 50mm"],
    "Elektronik": ["Widerstand 10k", "Kondensator 100uF", "LED rot", "Kabel 1m", "Sicherung 5A"],
    "Werkzeug" : ["Hammer", "Zange", "Schraubendreher", "Bohrer 6mm", "Sägeblatt"],
    "Verpackung" : ["Karton klein", "Karton groß", "Klebeband", "Folie 50m", "Polster"],
    "Hydraulik" : ["Schaluch 10mm", "Ventil DN20", "Dichtung", "Pumpe P100", "Filter HY5"]
}

def create_normal_product():
    """Erzeugt ein realistisches Produkt mit normalen Werten"""
    category_name = random.choice(list(KATEGORIEN.keys()))
    product_name = random.choice(KATEGORIEN[category_name])
    variant = random.randint(1, 100)

    return Inventory(
        product_name = f"{product_name}-{variant:03d}",
        quantity = random.randint(50, 1000),
        price = round(random.uniform(1.0, 50.0), 2),
        category = category_name,
        last_updated = datetime.now() - timedelta(days = random.randint(0, 90))
    )

def create_anomaly_product():
    """Erzeugt ein Produkt mit extremen Ausreißwerten."""
    category = random.choice(list(KATEGORIEN.keys()))
    product_name = random.choice(KATEGORIEN[category])

    if random.random() > 0.5:
        quantity = random.randint(5000, 15000)
        price = round(random.uniform(200.0, 999.99), 2)
    else:
        quantity = random.randint(1, 5)
        price = round(random.uniform(0.01, 0.1), 2)

    return Inventory(
        product_name = f"{product_name}-ANOMALIE",
        quantity = quantity,
        price = price,
        category = category,
        last_updated = datetime.now() - timedelta(days = random.randint(0, 90))
    )

def create_supplier(is_anomaly = False):
    """Erzeugt einen Lieferanten mit normalen oder extremen Werten"""
    company = ["Müller", "Schmidt", "Weber", "Fischer", "Wagner",
               "Becker", "Hoffmann", "Schulz", "Koch", "Richter"]
    legal_forms = ["GmbH", "AG", "KG", "OHG", "e.K."]

    name = f"{random.choice(company)} {random.choice(legal_forms)}-{random.randint(1,999):03d}"

    if  is_anomaly:
        return Supplier(
            name=name,
            delivery_reliability = round(random.uniform(0.0, 0.3), 2),
            avg_delivery_days = round(random.uniform(20.0, 45.0), 1),
            price_level = round(random.uniform(0.9, 1.0), 2),
            quality_score = round(random.uniform(0.0, 0.2), 2)
        )
    else:
        return Supplier(
            name = name,
            delivery_reliability = round(random.uniform(0.7, 0.99), 2),
            avg_delivery_days = round(random.uniform(2.0, 8.0), 1),
            price_level = round(random.uniform(0.3, 0.8), 2),
            quality_score = round(random.uniform(0.6, 0.98), 2)
        )

def generate_products(amount = 500, share_anomalies = 0.05):
    """Erzeugt eine Liste von Produkt-Objekten (ohne DB-Zugriff)"""
    amount_anomalies = int(amount * share_anomalies)
    amount_normal = amount - amount_anomalies

    products = []
    for _ in range(amount_normal):
        products.append(create_normal_product())
    for _ in range(amount_anomalies):
        products.append(create_anomaly_product())

    return products

def generate_suppliers(amount = 50, share_anomalies = 0.05):
    """Erzeugt eine Liste von Liefranten-Objekten (ohne DB-Zugriff)"""
    amount_anomalies = int(amount * share_anomalies)
    amount_normal = amount - amount_anomalies

    suppliers = []
    for _ in range(amount_normal):
        suppliers.append(create_supplier(is_anomaly=False))
    for _ in range(amount_anomalies):
        suppliers.append(create_supplier(is_anomaly=True))

    return suppliers

def add_data(db, amount_products = 500, amount_suppliers = 50):
    """Fügt neue Produkte und Liefranten der DB hinzu (ohne Löschen)."""

    # Zufällige Anomalierate zwischen 2% und 8%
    random_anomaly_rate = round(random.uniform(0.02, 0.08), 2)

    products = generate_products(amount_products, random_anomaly_rate)
    suppliers = generate_suppliers(amount_suppliers, random_anomaly_rate)

    db.add_all(products)
    db.add_all(suppliers)
    db.commit()

    return {
        "Produkte": len(products),
        "Lieferanten": len(suppliers),
        "Anomalie_Rate": random_anomaly_rate
    }

def seed():
    """HAUPTFUNKTION: Füllt die Datenbank mit Testdaten."""
    db = SessionLocal()

    try:
        # === Löschen der alten Daten ===
        db.query(Inventory).delete()
        db.query(Supplier).delete()
        db.commit()
        print("Alte Daten gelöscht.")

        # === Neue Lieferanten und Produkte hinzufügen ===
        result = add_data(db)
        print(f"{result['Produkte']} Produkte hinzugefügt.")
        print(f"{result['Lieferanten']} Liefranten hinzugefügt")
        print("Datenbank erfolgreich befüllt!")
    
    except Exception as e:
        db.rollback()
        print(f"Fehler beim Seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()