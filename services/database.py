import os
import sqlite3

from config import config


def maak_tabellen():
    """Maakt de tabellen aan als ze nog niet bestaan."""
    # Maak de map voor de database (bv. 'data') aan als die nog niet bestaat
    map_db = os.path.dirname(config.DB_PATH)
    if map_db:
        os.makedirs(map_db, exist_ok=True)

    with sqlite3.connect(config.DB_PATH) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS leveranciers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                naam TEXT NOT NULL UNIQUE,
                email TEXT
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS vragenlijsten (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                naam TEXT NOT NULL,
                leverancier_id INTEGER NOT NULL,
                afdeling TEXT NOT NULL,
                contactpersoon TEXT,
                startdatum TEXT,
                einddatum TEXT,
                opstartkost REAL,
                jaarlijkse_kost REAL,
                status TEXT NOT NULL DEFAULT 'aanvraag lopende'
                    CHECK (status IN ('aanvraag lopende', 'actief', 'opgezegd')),
                FOREIGN KEY (leverancier_id) REFERENCES leveranciers (id)
            )
        """)
    db.close()