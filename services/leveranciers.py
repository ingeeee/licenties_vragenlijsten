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


if __name__ == "__main__":
    for leverancier in alle_leveranciers():
        print(leverancier)
