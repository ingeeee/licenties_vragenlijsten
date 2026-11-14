"""Opzoekingen en wijzigingen voor de tabel vragenlijsten."""

import sqlite3

from config import config
from models.vragenlijst import Vragenlijst

# Basisquery: alle kolommen van vragenlijsten + de naam van de leverancier.
# Wordt hergebruikt door de verschillende opzoekfuncties.
BASIS_QUERY = """
    SELECT v.id, v.naam, v.leverancier_id, l.naam, v.afdeling, v.contactpersoon,
           v.startdatum, v.einddatum, v.opstartkost, v.jaarlijkse_kost, v.status
    FROM vragenlijsten AS v
    JOIN leveranciers AS l ON v.leverancier_id = l.id
"""


def rij_naar_vragenlijst(rij):
    """Maakt van een rij uit BASIS_QUERY een Vragenlijst-object."""
    (vragenlijst_id, naam, leverancier_id, leverancier_naam, afdeling, contactpersoon,
     startdatum, einddatum, opstartkost, jaarlijkse_kost, status) = rij
    return Vragenlijst(naam, leverancier_id, afdeling, contactpersoon,
                       startdatum, einddatum, opstartkost, jaarlijkse_kost, status,
                       vragenlijst_id=vragenlijst_id, leverancier_naam=leverancier_naam)


def alle_vragenlijsten():
    """Geeft alle vragenlijsten terug als lijst van Vragenlijst-objecten, gesorteerd op naam."""
    with sqlite3.connect(config.DB_PATH) as db:
        rijen = db.execute(BASIS_QUERY + " ORDER BY v.naam").fetchall()
    db.close()

    vragenlijsten = []
    for rij in rijen:
        vragenlijsten.append(rij_naar_vragenlijst(rij))
    return vragenlijsten


if __name__ == "__main__":
    for vragenlijst in alle_vragenlijsten():
        print(vragenlijst)
