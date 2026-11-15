"""Hulpfuncties voor invoer en uitvoer in de terminal."""

from models.vragenlijst import Vragenlijst
from services.leveranciers import alle_leveranciers
from services.vragenlijsten import alle_vragenlijsten, zoek_op_id


def toon_lijst(items):
    """Drukt elk item af, of een melding als de lijst leeg is."""
    if not items:
        print("Geen resultaten gevonden.")
    for item in items:
        print(item)


def toon_genummerd(items):
    """Drukt de items af met een volgnummer ervoor (1, 2, 3, ...)."""
    for nummer, item in enumerate(items, start=1):
        print(f"  {nummer}. {item}")


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


def kies_uit_lijst(items, vraag):
    """Toont een genummerde lijst en laat de gebruiker een nummer kiezen.

    Geeft het gekozen item terug.
    """
    toon_genummerd(items)
    while True:
        nummer = vraag_getal(vraag)
        if 1 <= nummer <= len(items):
            return items[nummer - 1]
        print("Ongeldige keuze.")


def kies_status():
    """Toont de mogelijke statussen en laat de gebruiker er een kiezen."""
    return kies_uit_lijst(Vragenlijst.STATUSSEN, "Typ het nummer van de status: ")


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


def kies_vragenlijst():
    """Toont alle vragenlijsten en laat de gebruiker er een kiezen via het id.

    Geeft het Vragenlijst-object terug, of None als het id niet bestaat.
    """
    toon_lijst(alle_vragenlijsten())
    vragenlijst = zoek_op_id(
        vraag_getal("\nTyp het id (het nummer tussen [ ]) van de vragenlijst: "))
    if vragenlijst is None:
        print("Er is geen vragenlijst met dit id.")
    return vragenlijst
