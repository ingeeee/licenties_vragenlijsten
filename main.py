"""Startpunt van de applicatie: een menu in de terminal."""

from models.vragenlijst import Vragenlijst
from services.database import maak_tabellen
from services.leveranciers import alle_leveranciers
from services.vragenlijsten import (alle_vragenlijsten, vervallend_binnen,
                                    zoek_op_afdeling, zoek_op_contactpersoon, zoek_op_leverancier,
                                    zoek_op_status)

MENU = """
=== Licenties vragenlijsten ===
1. Alle leveranciers tonen
2. Alle vragenlijsten tonen
3. Vragenlijsten zoeken (afdeling / leverancier / contactpersoon / status)
4. Licenties die binnenkort vervallen
0. Afsluiten"""


# Hulpfuncties voor het menu

def toon_lijst(items):
    """Drukt elk item af, of een melding als de lijst leeg is."""
    if not items:
        print("Geen resultaten gevonden.")
    for item in items:
        print(item)


def vraag_getal(vraag):
    """Blijft vragen tot de gebruiker een geheel getal ingeeft."""
    while True:
        antwoord = input(vraag).strip()
        if antwoord.isdigit():
            return int(antwoord)
        print("Gelieve een geheel getal in te geven.")


# De menu-opties

def menu_leveranciers():
    """Menu-optie 1: alle leveranciers tonen."""
    print("\n--- Leveranciers ---")
    toon_lijst(alle_leveranciers())


def menu_vragenlijsten():
    """Menu-optie 2: alle vragenlijsten tonen."""
    print("\n--- Vragenlijsten ---")
    toon_lijst(alle_vragenlijsten())


def menu_zoeken():
    """Menu-optie 3: vragenlijsten zoeken op afdeling, contactpersoon, leverancier of status."""
    print("\nZoeken op:")
    print("  a. afdeling")
    print("  b. leverancier")
    print("  c. contactpersoon")
    print("  d. status")
    keuze = input("Maak je keuze: ").strip().lower()

    if keuze == "a":
        afdeling = input("Afdeling (of een deel ervan): ")
        print()
        toon_lijst(zoek_op_afdeling(afdeling))

    elif keuze == "b":
        toon_lijst(alle_leveranciers())
        leverancier_id = vraag_getal("Id van de leverancier: ")
        print()
        toon_lijst(zoek_op_leverancier(leverancier_id))

    elif keuze == "c":
        contactpersoon = input("Contactpersoon (of een deel ervan): ")
        print()
        toon_lijst(zoek_op_contactpersoon(contactpersoon))

    elif keuze == "d":
        for nummer, status in enumerate(Vragenlijst.STATUSSEN, start=1):
            print(f"  {nummer}. {status}")
        nummer = vraag_getal("Kies een status: ")
        if 1 <= nummer <= len(Vragenlijst.STATUSSEN):
            print()
            toon_lijst(zoek_op_status(Vragenlijst.STATUSSEN[nummer - 1]))
        else:
            print("Ongeldige keuze.")

    else:
        print("Ongeldige keuze.")


def menu_vervallend():
    """Menu-optie 4: actieve licenties die binnen X dagen vervallen."""
    dagen = vraag_getal("Binnen hoeveel dagen? ")
    print(f"\n--- Actieve licenties die binnen {dagen} dagen vervallen ---")
    vervallend = vervallend_binnen(dagen)
    if not vervallend:
        print("Geen resultaten gevonden.")
    for vragenlijst in vervallend:
        print(vragenlijst, f"(nog {vragenlijst.dagen_tot_einddatum()} dagen)")


# Het hoofdprogramma

def main():
    """Toont het menu en voert de gekozen optie uit, tot de gebruiker afsluit."""
    maak_tabellen()

    while True:
        print(MENU)
        keuze = input("Maak je keuze: ").strip()

        if keuze == "1":
            menu_leveranciers()
        elif keuze == "2":
            menu_vragenlijsten()
        elif keuze == "3":
            menu_zoeken()
        elif keuze == "4":
            menu_vervallend()
        elif keuze == "0":
            print("Tot ziens!")
            break
        else:
            print("Ongeldige keuze, probeer opnieuw.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAfgesloten door Ctrl+C. Tot ziens!")
