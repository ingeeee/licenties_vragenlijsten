"""Hulpfuncties om datums en bedragen te controleren en om te zetten.

Worden gebruikt door de klasse Vragenlijst, de services en het menu.
"""

from datetime import datetime

# Formaat waarin de gebruiker datums intypt en te zien krijgt
DATUMFORMAAT = "%d-%m-%Y"      # DD-MM-JJJJ
# Formaat waarin datums in de database bewaard worden
DATABASEFORMAAT = "%Y-%m-%d"   # JJJJ-MM-DD


def controleer_datum(tekst):
    """Zet een datum in tekst om naar een date-object.

    Aanvaardt DD-MM-JJJJ (zoals de gebruiker ingeeft) en JJJJ-MM-DD (zoals in de database).
    Geeft None terug als er geen datum is ingevuld.
    """
    if not tekst:
        return None
    for formaat in (DATUMFORMAAT, DATABASEFORMAAT):
        try:
            return datetime.strptime(tekst.strip(), formaat).date()
        except ValueError:
            pass  # Als het ene formaat niet lukt, proberen we het andere
    raise ValueError(f"'{tekst}' is geen geldige datum (gebruik DD-MM-JJJJ).")


def datum_als_tekst(datum, leeg="?"):
    """Geeft een date-object terug als tekst DD-MM-JJJJ (of leeg als er geen datum is)."""
    return datum.strftime(DATUMFORMAAT) if datum else leeg


def datum_voor_database(datum):
    """Geeft een date-object terug als tekst JJJJ-MM-DD (of None als er geen datum is)."""
    return datum.strftime(DATABASEFORMAAT) if datum else None


def kost_als_tekst(kost, leeg="?"):
    """Geeft een kost terug als tekst (met 2 decimalen, komma voor decimalen).

    Geeft leeg terug als er geen kost is.
    """
    if kost is None:
        return leeg
    return f"{kost:.2f}".replace(".", ",")


def controleer_kost(kost):
    """Controleert een kost: leeg (None) of een getal van minstens 0.

    Bij invoer als tekst wordt de Belgische schrijfwijze gebruikt:
    een komma voor decimalen en geen punt.
    """
    if kost is None or kost == "":
        return None
    if isinstance(kost, str):
        if "." in kost:
            raise ValueError("Gebruik een komma voor decimalen, geen punt.")
        kost = kost.replace(",", ".")
    try:
        bedrag = float(kost)
    except ValueError as fout:
        raise ValueError(f"'{kost}' is geen geldig bedrag.") from fout
    if bedrag < 0:
        raise ValueError("Een kost kan niet negatief zijn.")
    return bedrag
