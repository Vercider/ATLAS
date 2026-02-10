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

def seed():
    """HAUPTFUNKTION: Füllt die Datenbank mit Testdaten."""
    db = SessionLocal()

    try:
        # === Löschen der alten Daten ===
        db.query(Inventory).delete()
        db.query(Supplier).delete()
        db.commit()
        print("Alte Daten gelöscht.")

        # === Produkte erzeugen ===
        amount_anomalies = int(ANZAHL_PRODUKTE * ANTEIL_ANOMALIEN)
        amount_normal = ANZAHL_PRODUKTE - amount_anomalies

        products = []
        for _ in range(amount_normal):
            products.append(create_normal_product())
        for _ in range(amount_anomalies):
            products.append(create_anomaly_product())

        db.add_all(products)
        print(f"{ANZAHL_PRODUKTE} Produkte erzeugt ({amount_anomalies} Anomalien).")

        # === Lieferanten erzeugen ===
        amount_anomaly_supplier = int(ANZAHL_LIEFERANTEN * ANTEIL_ANOMALIEN)
        amount_normal_supplier = ANZAHL_LIEFERANTEN - amount_anomaly_supplier

        suppliers = []
        for _ in range(amount_normal_supplier):
            suppliers.append(create_supplier(is_anomaly = False))
        for _ in range(amount_anomaly_supplier):
            suppliers.append(create_supplier(is_anomaly=True))

        db.add_all(suppliers)
        print(f"{ANZAHL_LIEFERANTEN} Lieferanten erzeugt ({amount_anomaly_supplier} Anomalien)")

        # === Alles speichern ===
        db.commit()
        print("\nSeeding abgeschlossen!")
    
    except Exception as e:
        db.rollback()
        print(f"Fehler beim Seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()