"""Maakt rapporten als csv-bestanden in de map uit de instellingen (RAPPORT_MAP)."""

import csv
import os
from datetime import date

from config import config
from models.omzetting import datum_als_tekst, kost_als_tekst
from services.vragenlijsten import alle_vragenlijsten, kosten_per_afdeling

# Instellingen zodat het bestand netjes opent in een Belgische Excel
SCHEIDINGSTEKEN = ";"
CODERING = "utf-8-sig"


def maak_bestandspad(naam):
    """Geeft het pad voor een nieuw rapport terug, bv. rapporten/vragenlijsten_2026-11-15.csv.

    Maakt de rapportmap aan als die nog niet bestaat.
    """
    os.makedirs(config.RAPPORT_MAP, exist_ok=True)
    return os.path.join(config.RAPPORT_MAP, f"{naam}_{date.today().isoformat()}.csv")


def rapport_alle_vragenlijsten():
    """Schrijft alle vragenlijsten met al hun gegevens naar een csv-bestand.

    Geeft het pad van het bestand terug.
    """
    pad = maak_bestandspad("vragenlijsten")
    with open(pad, "w", newline="", encoding=CODERING) as bestand:
        writer = csv.writer(bestand, delimiter=SCHEIDINGSTEKEN)
        writer.writerow(["Id", "Naam", "Leverancier", "Afdeling", "Contactpersoon",
                         "Status", "Startdatum", "Einddatum", "Dagen tot einddatum",
                         "Opstartkost", "Jaarlijkse kost"])
        for vragenlijst in alle_vragenlijsten():
            # Dagen tot einddatum enkel voor actieve licenties (negatief = al vervallen)
            dagen = None
            if vragenlijst.get_status() == "actief":
                dagen = vragenlijst.dagen_tot_einddatum()
            writer.writerow([
                vragenlijst.get_id(),
                vragenlijst.get_naam(),
                vragenlijst.get_leverancier_naam(),
                vragenlijst.get_afdeling(),
                vragenlijst.get_contactpersoon() or "",
                vragenlijst.get_status(),
                datum_als_tekst(vragenlijst.get_startdatum(), ""),
                datum_als_tekst(vragenlijst.get_einddatum(), ""),
                "" if dagen is None else dagen,
                kost_als_tekst(vragenlijst.get_opstartkost(), ""),
                kost_als_tekst(vragenlijst.get_jaarlijkse_kost(), ""),
            ])
    return pad


def rapport_kosten_per_afdeling():
    """Schrijft per afdeling het aantal actieve licenties en de totale jaarlijkse kost weg.

    Geeft het pad van het bestand terug.
    """
    pad = maak_bestandspad("kosten_per_afdeling")
    with open(pad, "w", newline="", encoding=CODERING) as bestand:
        writer = csv.writer(bestand, delimiter=SCHEIDINGSTEKEN)
        writer.writerow(["Afdeling", "Aantal actieve licenties", "Totale jaarlijkse kost"])
        for afdeling, aantal, totaal in kosten_per_afdeling():
            writer.writerow([afdeling, aantal, kost_als_tekst(totaal, "0,00")])
    return pad


if __name__ == "__main__":
    print("Rapport gemaakt:", rapport_alle_vragenlijsten())
    print("Rapport gemaakt:", rapport_kosten_per_afdeling())
