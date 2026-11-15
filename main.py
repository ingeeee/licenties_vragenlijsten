"""Startpunt van de applicatie: een menu in de terminal."""

from menu.opties import (menu_aanpassen, menu_details, menu_leveranciers,
                         menu_nieuwe_leverancier, menu_nieuwe_vragenlijst,
                         menu_overdragen, menu_rapport, menu_vervallend,
                         menu_vragenlijsten, menu_zoeken)
from services.database import maak_tabellen

MENU = """
=== Licenties vragenlijsten ===
Bekijken
  1. Alle leveranciers tonen
  2. Alle vragenlijsten tonen
  3. Details van een vragenlijst bekijken (ook de kosten)
  4. Vragenlijsten zoeken (afdeling / leverancier / contactpersoon / status)
  5. Licenties die binnenkort vervallen
Toevoegen
  6. Nieuwe leverancier toevoegen
  7. Nieuwe vragenlijst (of aanvraag) toevoegen
Wijzigen
  8. Vragenlijst aanpassen
  9. Contactpersoon overdragen (bv. bij vertrek van een collega)
Rapport
 10. Rapport maken (csv)

0. Afsluiten
"""


# Welke functie hoort bij welke keuze in het hoofdmenu
MENU_ACTIES = {
    "1": menu_leveranciers,
    "2": menu_vragenlijsten,
    "3": menu_details,
    "4": menu_zoeken,
    "5": menu_vervallend,
    "6": menu_nieuwe_leverancier,
    "7": menu_nieuwe_vragenlijst,
    "8": menu_aanpassen,
    "9": menu_overdragen,
    "10": menu_rapport,
}


def main():
    """Toont het menu en voert de gekozen optie uit, tot de gebruiker afsluit."""
    maak_tabellen()

    while True:
        print(MENU)
        keuze = input("Maak je keuze (geef het nummer in): ").strip()

        if keuze == "0":
            print("Tot ziens!")
            break

        actie = MENU_ACTIES.get(keuze)
        if actie is None:
            print("Ongeldige keuze, probeer opnieuw.")
        else:
            actie()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAfgesloten door Ctrl+C. Tot ziens!")
