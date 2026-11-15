"""Startpunt van de applicatie: een menu in de terminal."""

from models.leverancier import Leverancier
from models.vragenlijst import (Vragenlijst, controleer_datum, controleer_kost,
                                datum_als_tekst, kost_als_tekst)
from services.database import maak_tabellen
from services.leveranciers import (alle_leveranciers, leverancier_bestaat,
                                   voeg_leverancier_toe)
from services.rapporten import rapport_alle_vragenlijsten, rapport_kosten_per_afdeling
from services.vragenlijsten import (alle_contactpersonen, alle_vragenlijsten,
                                    draag_contactpersoon_over, vervallend_binnen,
                                    voeg_vragenlijst_toe, vragenlijsten_van_contactpersoon,
                                    wijzig_vragenlijst, zoek_op_afdeling,
                                    zoek_op_contactpersoon, zoek_op_id,
                                    zoek_op_leverancier, zoek_op_status)

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
    """Vraagt een nieuwe waarde voor een veld.

    Enter (leeg laten) behoudt de huidige waarde, een '-' maakt het veld leeg.
    Blijft vragen tot controle(antwoord) geen ValueError meer geeft.
    """
    while True:
        antwoord = input(f"{vraag} [{huidige_tekst or 'leeg'}]: ").strip()
        if not antwoord:
            antwoord = huidige_tekst
        elif antwoord == "-":
            antwoord = ""
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
        leverancier_id = vraag_getal("Typ het id (het nummer tussen [ ]) van de leverancier: ")
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


def menu_details():
    """Menu-optie 3: alle gegevens van één vragenlijst bekijken, ook de kosten."""
    print("\n--- Details van een vragenlijst ---")
    toon_lijst(alle_vragenlijsten())
    vragenlijst = zoek_op_id(
        vraag_getal("\nTyp het id (het nummer tussen [ ]) van de vragenlijst: "))
    if vragenlijst is None:
        print("Er is geen vragenlijst met dit id.")
        return
    print()
    print(vragenlijst.details())


def menu_zoeken():
    """Menu-optie 4: vragenlijsten zoeken op afdeling, leverancier, contactpersoon of status."""
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
    """Menu-optie 5: actieve licenties die binnen X dagen vervallen."""
    dagen = vraag_getal("Binnen hoeveel dagen? ")
    print(f"\n--- Actieve licenties die binnen {dagen} dagen vervallen ---")
    vervallend = vervallend_binnen(dagen)
    if not vervallend:
        print("Geen resultaten gevonden.")
    for vragenlijst in vervallend:
        print(vragenlijst, f"(nog {vragenlijst.dagen_tot_einddatum()} dagen)")


def menu_nieuwe_leverancier():
    """Menu-optie 6: een nieuwe leverancier toevoegen."""
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
    """Menu-optie 7: een nieuwe vragenlijst (of aanvraag) toevoegen."""
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
    """Menu-optie 8: een bestaande vragenlijst aanpassen."""
    print("\n--- Vragenlijst aanpassen ---")
    toon_lijst(alle_vragenlijsten())
    vragenlijst = zoek_op_id(
        vraag_getal("\nTyp het id (het nummer tussen [ ]) van de vragenlijst: "))
    if vragenlijst is None:
        print("Er is geen vragenlijst met dit id.")
        return

    print("Tip: Enter = huidige waarde [tussen haakjes] behouden, '-' maakt het veld leeg.")
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


def menu_overdragen():
    """Menu-optie 9: alle vragenlijsten van een contactpersoon overdragen aan iemand anders."""
    print("\n--- Contactpersoon overdragen ---")
    contactpersonen = alle_contactpersonen()
    if not contactpersonen:
        print("Er zijn nog geen contactpersonen.")
        return

    # Stap 1: de huidige contactpersoon kiezen uit een genummerde lijst
    for nummer, contactpersoon in enumerate(contactpersonen, start=1):
        print(f"  {nummer}. {contactpersoon}")
    nummer = vraag_getal("Typ het nummer van de contactpersoon die je wil vervangen: ")
    if not 1 <= nummer <= len(contactpersonen):
        print("Ongeldige keuze.")
        return
    oude = contactpersonen[nummer - 1]

    # Stap 2: tonen wat er zal veranderen
    print(f"\nVragenlijsten van {oude}:")
    toon_lijst(vragenlijsten_van_contactpersoon(oude))

    # Stap 3: de nieuwe contactpersoon kiezen (bestaand) of typen (nieuw)
    print("\nNieuwe contactpersoon:")
    for nummer, contactpersoon in enumerate(contactpersonen, start=1):
        print(f"  {nummer}. {contactpersoon}")
    antwoord = input("Typ het NUMMER van een bestaande contactpersoon of de NAAM van "
                     "een nieuwe (leeg laten om te annuleren): ").strip()
    if not antwoord:
        print("Overdragen geannuleerd.")
        return
    if antwoord.isdigit() and 1 <= int(antwoord) <= len(contactpersonen):
        nieuwe = contactpersonen[int(antwoord) - 1]
    else:
        nieuwe = antwoord
    if nieuwe == oude:
        print("De nieuwe contactpersoon is dezelfde als de huidige. Er verandert niets.")
        return

    # Stap 4: bevestigen en uitvoeren
    bevestiging = input(f"Alles van {oude} overdragen aan {nieuwe}? (j/n): ").strip().lower()
    if bevestiging != "j":
        print("Overdragen geannuleerd.")
        return
    aantal = draag_contactpersoon_over(oude, nieuwe)
    print(f"{aantal} vragenlijst(en) overgedragen van {oude} aan {nieuwe}.")


def menu_rapport():
    """Menu-optie 10: een rapport als csv-bestand maken."""
    print("\nWelk rapport wil je maken?")
    print("  1. Alle vragenlijsten (met leverancier, datums, kosten en dagen tot einddatum)")
    print("  2. Kosten per afdeling (actieve licenties)")
    keuze = input("Maak je keuze: ").strip()

    if keuze == "1":
        pad = rapport_alle_vragenlijsten()
    elif keuze == "2":
        pad = rapport_kosten_per_afdeling()
    else:
        print("Ongeldige keuze.")
        return
    print(f"Rapport opgeslagen in: {pad}")


# Het hoofdprogramma

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
        keuze = input("Maak je keuze: ").strip()

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
