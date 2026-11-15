"""Opzoekingen en wijzigingen voor de tabel leveranciers."""

import sqlite3

from config import config
from models.leverancier import Leverancier


def alle_leveranciers():
    """Geeft alle leveranciers terug als lijst van Leverancier-objecten, gesorteerd op naam."""
    with sqlite3.connect(config.DB_PATH) as db:
        query = """
            SELECT id, naam, email
            FROM leveranciers
            ORDER BY naam
        """
        rijen = db.execute(query).fetchall()
    db.close()

    leveranciers = []
    for leverancier_id, naam, email in rijen:
        leveranciers.append(Leverancier(naam, email, leverancier_id))
    return leveranciers


def leverancier_bestaat(naam):
    """Geeft True als er al een leverancier met deze naam bestaat (hoofdletters tellen niet)."""
    with sqlite3.connect(config.DB_PATH) as db:
        rij = db.execute(
            "SELECT id FROM leveranciers WHERE LOWER(naam) = LOWER(?)",
            (naam.strip(),),
        ).fetchone()
    db.close()
    return rij is not None


def voeg_leverancier_toe(nieuwe_leverancier):
    """Slaat een nieuwe leverancier op in de database en geeft het nieuwe id terug.

    Geeft een ValueError als er al een leverancier met dezelfde naam bestaat.
    """
    try:
        with sqlite3.connect(config.DB_PATH) as db:
            cursor = db.execute(
                "INSERT INTO leveranciers (naam, email) VALUES (?, ?)",
                (nieuwe_leverancier.get_naam(), nieuwe_leverancier.get_email()),
            )
            nieuw_id = cursor.lastrowid
        db.close()
    except sqlite3.IntegrityError as fout:
        raise ValueError(
            f"Er bestaat al een leverancier met de naam '{nieuwe_leverancier.get_naam()}'."
        ) from fout
    return nieuw_id


if __name__ == "__main__":
    for leverancier in alle_leveranciers():
        print(leverancier)
