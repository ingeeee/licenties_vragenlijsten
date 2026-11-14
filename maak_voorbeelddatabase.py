"""Maakt de database aan en vult ze met voorbeeldgegevens.

Eenmalig uitvoeren vanuit de projectmap:  python maak_voorbeelddatabase.py
"""


import sqlite3

from config import config
from services.database import maak_tabellen

# (naam, email) - e-mailadressen zijn verzonnen
LEVERANCIERS = [
    ("Mapi Research Trust (ePROVIDE)", "licenties@voorbeeld-eprovide.org"),
    ("Oxford University Innovation", "licenties@voorbeeld-oxford.org"),
    ("PROM Solutions BV", None),
]

# (naam, leverancier, afdeling, contactpersoon, startdatum, einddatum,
#  opstartkost, jaarlijkse_kost, status) - alle gegevens zijn fictief
VRAGENLIJSTEN = [
    ("WOMAC", "Mapi Research Trust (ePROVIDE)", "Orthopedie", "An Peeters",
     "2024-01-01", "2026-12-31", 250.0, 900.0, "actief"),
    ("Oxford Knee Score", "Oxford University Innovation", "Orthopedie",
     "An Peeters", "2025-03-01", "2028-02-28", 0.0, 450.0, "actief"),
    ("Oxford Hip Score", "Oxford University Innovation", "Orthopedie", None,
     None, None, None, None, "aanvraag lopende"),
    ("Rugpijn-vragenlijst", "PROM Solutions BV", "Fysiotherapie", "Tom Claes",
     "2023-06-01", "2025-05-31", 500.0, 1200.0, "opgezegd"),
    ("Hartfalen-vragenlijst", "Mapi Research Trust (ePROVIDE)", "Cardiologie",
     "Sara De Smet", None, None, None, None, "aanvraag lopende"),
]


def vul_voorbeeldgegevens():
    """Voegt de voorbeeldgegevens toe als de database nog leeg is."""
    with sqlite3.connect(config.DB_PATH) as db:
        aantal = db.execute("SELECT COUNT(*) FROM leveranciers").fetchone()[0]

        if aantal == 0:
            for naam, email in LEVERANCIERS:
                db.execute(
                    "INSERT INTO leveranciers (naam, email) VALUES (?, ?)",
                    (naam, email),
                )

            for (naam, leverancier, afdeling, contactpersoon, startdatum,
                 einddatum, opstartkost, jaarlijkse_kost, status) in VRAGENLIJSTEN:
                db.execute(
                    """
                    INSERT INTO vragenlijsten (naam, leverancier_id, afdeling,
                        contactpersoon, startdatum, einddatum, opstartkost,
                        jaarlijkse_kost, status)
                    VALUES (?, (SELECT id FROM leveranciers WHERE naam = ?),
                        ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (naam, leverancier, afdeling, contactpersoon, startdatum,
                     einddatum, opstartkost, jaarlijkse_kost, status),
                )
    db.close()

    if aantal == 0:
        print("Voorbeeldgegevens toegevoegd.")
    else:
        print("De database bevat al gegevens: er werd niets toegevoegd.")


if __name__ == "__main__":
    maak_tabellen()
    vul_voorbeeldgegevens()
