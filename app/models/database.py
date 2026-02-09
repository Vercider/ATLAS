# === IMPORTE ===
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# === 1.DATENBANKLOKALISIERUNG ===
DATABASE_URL = "sqlite:///./atlas.db"

# === 2.DATENABNKVERBINDUNG ===
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# === 3.DATENBANKKOMMUNIKATION ===
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# === 4. BAIS-KLASSE ERSCHAFFEN ===
Base = declarative_base()
