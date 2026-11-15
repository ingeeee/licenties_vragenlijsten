"""De functies achter de keuzes in het hoofdmenu."""

from models.leverancier import Leverancier
from models.omzetting import (controleer_datum, controleer_kost, datum_als_tekst,
                              kost_als_tekst)
from models.vragenlijst import Vragenlijst
from menu.invoer import (kies_leverancier, kies_status, kies_uit_lijst, kies_vragenlijst,
                         toon_genummerd, toon_lijst, vraag_getal, vraag_tot_geldig,
                         vraag_wijziging)
from services.leveranciers import alle_leveranciers, leverancier_bestaat, voeg_leverancier_toe
from services.rapporten import rapport_alle_vragenlijsten, rapport_kosten_per_afdeling
from services.vragenlijsten import (alle_contactpersonen, alle_vragenlijsten,
                                    draag_contactpersoon_over, vervallend_binnen,
                                    voeg_vragenlijst_toe, vragenlijsten_van_contactpersoon,
                                    wijzig_vragenlijst, zoek_op_afdeling,
                                    zoek_op_contactpersoon, zoek_op_leverancier,
                                    zoek_op_status)


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
    vragenlijst = kies_vragenlijst()
    if vragenlijst is not None:
        print()
        print(vragenlijst.details())


def menu_zoeken():
    """Menu-optie 4: vragenlijsten zoeken op afdeling, leverancier, contactpersoon of status."""
    print("\nZoeken op:")
    print("  a. afdeling")
    print("  b. leverancier")
    print("  c. contactpersoon")
    print("  d. status")
    keuze = input("Maak je keuze (geef de letter in): ").strip().lower()

    if keuze == "a":
        afdeling = input("Afdeling (of een deel ervan): ")
        print()
        toon_lijst(zoek_op_afdeling(afdeling))

    elif keuze == "b":
        if not alle_leveranciers():
            print("Er zijn nog geen leveranciers.")
            return
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
    vraag_tot_geldig("E-mailadres (leeg laten als je het niet kent): ", leverancier.set_email)

    nieuw_id = voeg_leverancier_toe(leverancier)
    print(f"Leverancier '{leverancier.get_naam()}' toegevoegd met id {nieuw_id}.")


def menu_nieuwe_vragenlijst():
    """Menu-optie 7: een nieuwe vragenlijst (of aanvraag) toevoegen."""
    print("\n--- Nieuwe vragenlijst ---")

    if not alle_leveranciers():
        print("Voeg eerst een leverancier toe (optie 6).")
        return

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
    vragenlijst = kies_vragenlijst()
    if vragenlijst is None:
        return

    print("Tip: Enter = huidige waarde [tussen haakjes] behouden, '-' maakt het veld leeg.")
    while True:
        print("\n" + vragenlijst.details())
        print(MENU_AANPASSEN)
        keuze = input("Maak je keuze (geef het nummer in): ").strip()

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
    oude = kies_uit_lijst(contactpersonen,
                          "Typ het nummer van de contactpersoon die je wilt vervangen: ")

    # Stap 2: tonen wat er zal veranderen
    print(f"\nVragenlijsten van {oude}:")
    toon_lijst(vragenlijsten_van_contactpersoon(oude))

    # Stap 3: de nieuwe contactpersoon kiezen (bestaand) of typen (nieuw)
    print("\nNieuwe contactpersoon:")
    toon_genummerd(contactpersonen)
    antwoord = input("Typ het NUMMER van een bestaande contactpersoon of de NAAM van "
                     "een nieuwe (leeg laten om te annuleren): ").strip()
    if not antwoord:
        print("Overdragen geannuleerd.")
        return
    if antwoord.isdigit():
        # Een getal is altijd een keuze uit de lijst, nooit een naam van een nieuwe contactpersoon
        if not 1 <= int(antwoord) <= len(contactpersonen):
            print("Ongeldig nummer. Overdragen geannuleerd.")
            return
        nieuwe = contactpersonen[int(antwoord) - 1]
    else:
        nieuwe = antwoord
        # Bestaat deze naam al (hoofdletters niet meegerekend)?
        # Gebruik dan de bestaande schrijfwijze.
        for contactpersoon in contactpersonen:
            if contactpersoon.lower() == antwoord.lower():
                nieuwe = contactpersoon
                break
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
    keuze = input("Maak je keuze (geef het nummer in): ").strip()

    if keuze == "1":
        pad = rapport_alle_vragenlijsten()
    elif keuze == "2":
        pad = rapport_kosten_per_afdeling()
    else:
        print("Ongeldige keuze.")
        return
    print(f"Rapport opgeslagen in: {pad}")
