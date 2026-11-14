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


def zoek_vragenlijsten(voorwaarde="", parameters=()):
    """Voert BASIS_QUERY uit met een optionele WHERE-voorwaarde.

    Geeft een lijst van Vragenlijst-objecten terug, gesorteerd op naam.
    """
    query = BASIS_QUERY + voorwaarde + " ORDER BY v.naam"
    with sqlite3.connect(config.DB_PATH) as db:
        rijen = db.execute(query, parameters).fetchall()
    db.close()

    vragenlijsten = []
    for rij in rijen:
        vragenlijsten.append(rij_naar_vragenlijst(rij))
    return vragenlijsten


def alle_vragenlijsten():
    """Geeft alle vragenlijsten terug."""
    return zoek_vragenlijsten()


def zoek_op_afdeling(afdeling):
    """Geeft de vragenlijsten van een afdeling terug (deel van de naam volstaat)."""
    return zoek_vragenlijsten(" WHERE v.afdeling LIKE ?", (f"%{afdeling}%",))

def zoek_op_contactpersoon(contactpersoon):
    """Geeft de vragenlijsten van een contactpersoon terug (deel van de naam volstaat)."""
    return zoek_vragenlijsten(" WHERE v.contactpersoon LIKE ?", (f"%{contactpersoon}%",))

def zoek_op_leverancier(leverancier_id):
    """Geeft de vragenlijsten van een leverancier terug."""
    return zoek_vragenlijsten(" WHERE v.leverancier_id = ?", (leverancier_id,))


def zoek_op_status(status):
    """Geeft de vragenlijsten met een bepaalde status terug."""
    return zoek_vragenlijsten(" WHERE v.status = ?", (status,))


def vervallend_binnen(aantal_dagen):
    """Geeft de actieve vragenlijsten die binnen aantal_dagen vervallen.

    Gesorteerd op einddatum: wat het eerst vervalt, staat bovenaan.
    """
    vervallend = []
    for kandidaat in alle_vragenlijsten():
        if kandidaat.vervalt_binnen(aantal_dagen):
            vervallend.append(kandidaat)
    # Sorteer op einddatum: wat het eerst vervalt, staat bovenaan
    vervallend.sort(key=lambda item: item.get_einddatum())
    return vervallend


if __name__ == "__main__":
    print("--- Alle vragenlijsten ---")
    for vragenlijst in alle_vragenlijsten():
        print(vragenlijst)

    print("\n--- Afdeling 'ortho' ---")
    for vragenlijst in zoek_op_afdeling("ortho"):
        print(vragenlijst)

    print("\n--- Contactpersoon 'Jansen' ---")
    for vragenlijst in zoek_op_contactpersoon("Jansen"):
        print(vragenlijst)

    print("\n--- Leverancier 2 ---")
    for vragenlijst in zoek_op_leverancier(2):
        print(vragenlijst)

    print("\n--- Status 'aanvraag lopende' ---")
    for vragenlijst in zoek_op_status("aanvraag lopende"):
        print(vragenlijst)

    print("\n--- Vervallend binnen 90 dagen ---")
    for vragenlijst in vervallend_binnen(90):
        print(vragenlijst, f"(nog {vragenlijst.dagen_tot_einddatum()} dagen)")
