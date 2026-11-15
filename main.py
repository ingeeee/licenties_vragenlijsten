"""Startpunt van de applicatie: een menu in de terminal."""

from models.leverancier import Leverancier
from models.vragenlijst import (Vragenlijst, controleer_datum, controleer_kost,
                                datum_als_tekst, kost_als_tekst)
from services.database import maak_tabellen
from services.leveranciers import (alle_leveranciers, leverancier_bestaat,
                                   voeg_leverancier_toe)
from services.vragenlijsten import (alle_vragenlijsten, vervallend_binnen, voeg_vragenlijst_toe,
                                    wijzig_vragenlijst, zoek_op_afdeling, zoek_op_contactpersoon,
                                    zoek_op_id, zoek_op_leverancier, zoek_op_status)

MENU = """
=== Licenties vragenlijsten ===
1. Alle leveranciers tonen
2. Alle vragenlijsten tonen
3. Vragenlijsten zoeken (afdeling / leverancier / contactpersoon / status)
4. Licenties die binnenkort vervallen
5. Nieuwe leverancier toevoegen
6. Nieuwe vragenlijst (of aanvraag) toevoegen
7. Vragenlijst aanpassen
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


def vraag_tot_geldig(vraag, controle):
    """Blijft vragen tot controle(antwoord) geen ValueError meer geeft.

    Geeft het geldige antwoord terug.
    """
    while True:
        antwoord = input(vraag).strip()
        try:
            controle(antwoord)
            return antwoord
        except ValueError as fout:
            print(fout)


def vraag_wijziging(vraag, huidige_tekst, controle):
    """Vraagt een nieuwe waarde voor een veld, of Enter om de huidige waarde te behouden.

    Blijft vragen tot controle(antwoord) geen ValueError meer geeft.
    """
    while True:
        antwoord = input(f"{vraag} [{huidige_tekst or 'leeg'}]: ").strip()
        if not antwoord:
            antwoord = huidige_tekst
        try:
            controle(antwoord)
            return antwoord
        except ValueError as fout:
            print(fout)


def kies_leverancier():
    """Toont de leveranciers en laat de gebruiker er een kiezen.

    Geeft het gekozen Leverancier-object terug.
    """
    leveranciers = alle_leveranciers()
    toon_lijst(leveranciers)
    while True:
        leverancier_id = vraag_getal("Id van de leverancier: ")
        for leverancier in leveranciers:
            if leverancier.get_id() == leverancier_id:
                return leverancier
        print("Er is geen leverancier met dit id.")


def kies_status():
    """Toont de mogelijke statussen en laat de gebruiker er een kiezen."""
    for nummer, status in enumerate(Vragenlijst.STATUSSEN, start=1):
        print(f"  {nummer}. {status}")
    while True:
        nummer = vraag_getal("Kies een status: ")
        if 1 <= nummer <= len(Vragenlijst.STATUSSEN):
            return Vragenlijst.STATUSSEN[nummer - 1]
        print("Ongeldige keuze.")


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
    """Menu-optie 3: vragenlijsten zoeken op afdeling, leverancier, contactpersoon of status."""
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
        leverancier = kies_leverancier()
        print()
        toon_lijst(zoek_op_leverancier(leverancier.get_id()))

    elif keuze == "c":
        contactpersoon = input("Contactpersoon (of een deel ervan): ")
        print()
        toon_lijst(zoek_op_contactpersoon(contactpersoon))

    elif keuze == "d":
        status = kies_status()
        print()
        toon_lijst(zoek_op_status(status))

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


def menu_nieuwe_leverancier():
    """Menu-optie 5: een nieuwe leverancier toevoegen."""
    print("\n--- Nieuwe leverancier ---")

    # Naam (+ controle)
    naam = input("Naam (leeg laten om te annuleren): ").strip()
    if not naam:
        print("Toevoegen geannuleerd.")
        return
    if leverancier_bestaat(naam):
        print(f"Er bestaat al een leverancier met de naam '{naam}'.")
        return
    leverancier = Leverancier(naam)

    # E-mailadres (opnieuw vragen zolang het ongeldig is)
    while True:
        email = input("E-mailadres (leeg laten als je het niet kent): ")
        try:
            leverancier.set_email(email)
            break
        except ValueError as fout:
            print(fout)

    nieuw_id = voeg_leverancier_toe(leverancier)
    print(f"Leverancier '{leverancier.get_naam()}' toegevoegd met id {nieuw_id}.")


def menu_nieuwe_vragenlijst():
    """Menu-optie 6: een nieuwe vragenlijst (of aanvraag) toevoegen."""
    print("\n--- Nieuwe vragenlijst ---")

    naam = input("Naam van de vragenlijst (leeg laten om te annuleren): ").strip()
    if not naam:
        print("Toevoegen geannuleerd.")
        return

    print("\nLeverancier:")
    leverancier = kies_leverancier()

    while True:
        try:
            vragenlijst = Vragenlijst(naam, leverancier.get_id(), input("Afdeling: "),
                                      leverancier_naam=leverancier.get_naam())
            break
        except ValueError as fout:
            print(fout)

    vragenlijst.set_contactpersoon(input("Contactpersoon (mag leeg): "))

    print("\nStatus:")
    vragenlijst.set_status(kies_status())

    print("\nDatums in de vorm DD-MM-JJJJ (leeg laten als ze nog niet gekend zijn)")
    startdatum = vraag_tot_geldig("Startdatum: ", controleer_datum)
    vraag_tot_geldig("Einddatum: ",
                     lambda einddatum: vragenlijst.set_periode(startdatum, einddatum))

    print("\nKosten in euro (leeg laten als ze nog niet gekend zijn)")
    opstartkost = vraag_tot_geldig("Opstartkost: ", controleer_kost)
    vraag_tot_geldig("Jaarlijkse kost: ",
                     lambda jaarlijkse_kost: vragenlijst.set_kosten(opstartkost, jaarlijkse_kost))

    nieuw_id = voeg_vragenlijst_toe(vragenlijst)
    print(f"\nVragenlijst '{vragenlijst.get_naam()}' toegevoegd met id {nieuw_id}.")


MENU_AANPASSEN = """
Wat wil je aanpassen?
  1. Naam
  2. Leverancier
  3. Afdeling
  4. Contactpersoon
  5. Status
  6. Periode (start- en einddatum)
  7. Kosten
  0. Opslaan en terug naar het hoofdmenu
  9. Annuleren (niets opslaan)"""


def menu_aanpassen():
    """Menu-optie 7: een bestaande vragenlijst aanpassen."""
    print("\n--- Vragenlijst aanpassen ---")
    toon_lijst(alle_vragenlijsten())
    vragenlijst = zoek_op_id(vraag_getal("\nId van de vragenlijst: "))
    if vragenlijst is None:
        print("Er is geen vragenlijst met dit id.")
        return

    print("Tip: druk op Enter om de huidige waarde [tussen haakjes] te behouden.")
    while True:
        print("\n" + vragenlijst.details())
        print(MENU_AANPASSEN)
        keuze = input("Maak je keuze: ").strip()

        if keuze == "1":
            vraag_wijziging("Naam", vragenlijst.get_naam(), vragenlijst.set_naam)

        elif keuze == "2":
            leverancier = kies_leverancier()
            vragenlijst.set_leverancier(leverancier.get_id(), leverancier.get_naam())

        elif keuze == "3":
            vraag_wijziging("Afdeling", vragenlijst.get_afdeling(), vragenlijst.set_afdeling)

        elif keuze == "4":
            vraag_wijziging("Contactpersoon", vragenlijst.get_contactpersoon() or "",
                            vragenlijst.set_contactpersoon)

        elif keuze == "5":
            vragenlijst.set_status(kies_status())

        elif keuze == "6":
            startdatum = vraag_wijziging("Startdatum (DD-MM-JJJJ)",
                                         datum_als_tekst(vragenlijst.get_startdatum(), ""),
                                         controleer_datum)
            vraag_wijziging("Einddatum (DD-MM-JJJJ)",
                            datum_als_tekst(vragenlijst.get_einddatum(), ""),
                            lambda einddatum: vragenlijst.set_periode(startdatum, einddatum))

        elif keuze == "7":
            opstartkost = vraag_wijziging("Opstartkost",
                                          kost_als_tekst(vragenlijst.get_opstartkost(), ""),
                                          controleer_kost)
            vraag_wijziging("Jaarlijkse kost",
                            kost_als_tekst(vragenlijst.get_jaarlijkse_kost(), ""),
                            lambda kost: vragenlijst.set_kosten(opstartkost, kost))

        elif keuze == "0":
            wijzig_vragenlijst(vragenlijst)
            print(f"De wijzigingen aan '{vragenlijst.get_naam()}' zijn opgeslagen.")
            return

        elif keuze == "9":
            print("Aanpassen geannuleerd, er werd niets opgeslagen.")
            return

        else:
            print("Ongeldige keuze.")


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
        elif keuze == "5":
            menu_nieuwe_leverancier()
        elif keuze == "6":
            menu_nieuwe_vragenlijst()
        elif keuze == "7":
            menu_aanpassen()
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
