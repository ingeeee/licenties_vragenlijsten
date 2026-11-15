"""Maakt de database aan en vult ze met voorbeeldgegevens.

Eenmalig uitvoeren vanuit de projectmap:  python maak_voorbeelddatabase.py
"""

from models.leverancier import Leverancier
from models.vragenlijst import Vragenlijst
from services.database import maak_tabellen
from services.leveranciers import alle_leveranciers, voeg_leverancier_toe
from services.vragenlijsten import voeg_vragenlijst_toe

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
     "01-01-2024", "31-12-2026", 250.0, 900.0, "actief"),
    ("Oxford Knee Score", "Oxford University Innovation", "Orthopedie",
     "An Peeters", "01-03-2025", "28-02-2028", 0.0, 450.0, "actief"),
    ("Oxford Hip Score", "Oxford University Innovation", "Orthopedie", None,
     None, None, None, None, "aanvraag lopende"),
    ("Rugpijn-vragenlijst", "PROM Solutions BV", "Fysiotherapie", "Tom Claes",
     "01-06-2023", "31-05-2025", 500.0, 1200.0, "opgezegd"),
    ("Hartfalen-vragenlijst", "Mapi Research Trust (ePROVIDE)", "Cardiologie",
     "Sara De Smet", None, None, None, None, "aanvraag lopende"),
]


def vul_voorbeeldgegevens():
    """Voegt de voorbeeldgegevens toe als de database nog leeg is."""
    if alle_leveranciers():
        print("De database bevat al gegevens: er werd niets toegevoegd.")
        return

    # Leveranciers toevoegen en onthouden welk id elke leverancier kreeg
    leverancier_ids = {}
    for naam, email in LEVERANCIERS:
        leverancier_ids[naam] = voeg_leverancier_toe(Leverancier(naam, email))

    # Vragenlijsten toevoegen, gekoppeld aan het id van hun leverancier
    for (naam, leverancier, afdeling, contactpersoon, startdatum, einddatum,
         opstartkost, jaarlijkse_kost, status) in VRAGENLIJSTEN:
        vragenlijst = Vragenlijst(naam, leverancier_ids[leverancier], afdeling,
                                  contactpersoon, startdatum, einddatum,
                                  opstartkost, jaarlijkse_kost, status)
        voeg_vragenlijst_toe(vragenlijst)

    print("Voorbeeldgegevens toegevoegd.")


if __name__ == "__main__":
    maak_tabellen()
    vul_voorbeeldgegevens()
