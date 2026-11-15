"""Bevat de klasse Vragenlijst."""

from datetime import date

from models.omzetting import (controleer_datum, controleer_kost, datum_als_tekst,
                              datum_voor_database, kost_als_tekst)


# De klasse volgt de kolommen van de tabel, vandaar veel attributen, parameters en methodes.
# pylint: disable=too-many-instance-attributes,too-many-arguments
# pylint: disable=too-many-positional-arguments,too-many-public-methods
class Vragenlijst:
    """Een licentie (of aanvraag) voor een vragenlijst bij een leverancier."""

    # Klasseattribuut: de toegelaten statussen, gedeeld door alle vragenlijsten
    STATUSSEN = ("aanvraag lopende", "actief", "opgezegd")

    def __init__(self, naam, leverancier_id, afdeling,
                 contactpersoon=None, startdatum=None, einddatum=None,
                 opstartkost=None, jaarlijkse_kost=None,
                 status="aanvraag lopende", vragenlijst_id=None,
                 leverancier_naam=None):
        self.__id = vragenlijst_id
        self.__leverancier_id = leverancier_id
        self.__leverancier_naam = leverancier_naam
        self.set_naam(naam)
        self.set_afdeling(afdeling)
        self.set_contactpersoon(contactpersoon)
        self.set_periode(startdatum, einddatum)
        self.set_kosten(opstartkost, jaarlijkse_kost)
        self.set_status(status)

    # Getters

    def get_id(self):
        """Geeft het id terug (None als nog niet opgeslagen)."""
        return self.__id

    def get_naam(self):
        """Geeft de naam van de vragenlijst terug."""
        return self.__naam

    def get_leverancier_id(self):
        """Geeft het id van de leverancier terug."""
        return self.__leverancier_id

    def get_leverancier_naam(self):
        """Geeft de naam van de leverancier terug (indien gekend)."""
        return self.__leverancier_naam

    def get_afdeling(self):
        """Geeft de afdeling terug."""
        return self.__afdeling

    def get_contactpersoon(self):
        """Geeft de contactpersoon terug (None als er geen is)."""
        return self.__contactpersoon

    def get_startdatum(self):
        """Geeft de startdatum terug als date-object (of None)."""
        return self.__startdatum

    def get_einddatum(self):
        """Geeft de einddatum terug als date-object (of None)."""
        return self.__einddatum

    def get_opstartkost(self):
        """Geeft de eenmalige opstartkost terug (of None)."""
        return self.__opstartkost

    def get_jaarlijkse_kost(self):
        """Geeft de jaarlijkse kost terug (of None)."""
        return self.__jaarlijkse_kost

    def get_status(self):
        """Geeft de status terug."""
        return self.__status

    # Setters

    def set_naam(self, naam):
        """Stelt de naam in. De naam mag niet leeg zijn."""
        if not naam or not naam.strip():
            raise ValueError("De naam van de vragenlijst mag niet leeg zijn.")
        self.__naam = naam.strip()

    def set_leverancier(self, leverancier_id, leverancier_naam=None):
        """Koppelt de vragenlijst aan een (andere) leverancier."""
        self.__leverancier_id = leverancier_id
        self.__leverancier_naam = leverancier_naam

    def set_afdeling(self, afdeling):
        """Stelt de afdeling in. De afdeling mag niet leeg zijn."""
        if not afdeling or not afdeling.strip():
            raise ValueError("De afdeling mag niet leeg zijn.")
        self.__afdeling = afdeling.strip()

    def set_contactpersoon(self, contactpersoon):
        """Stelt de contactpersoon in (mag leeg zijn)."""
        self.__contactpersoon = contactpersoon.strip() if contactpersoon else None

    def set_periode(self, startdatum, einddatum):
        """Stelt start- en einddatum in.

        Beide mogen leeg zijn, maar de einddatum mag niet voor de startdatum liggen.
        """
        startdatum = controleer_datum(startdatum)
        einddatum = controleer_datum(einddatum)
        if startdatum and einddatum and einddatum < startdatum:
            raise ValueError("De einddatum mag niet voor de startdatum liggen.")
        self.__startdatum = startdatum
        self.__einddatum = einddatum

    def set_kosten(self, opstartkost, jaarlijkse_kost):
        """Stelt de opstartkost en de jaarlijkse kost in (mogen leeg zijn)."""
        self.__opstartkost = controleer_kost(opstartkost)
        self.__jaarlijkse_kost = controleer_kost(jaarlijkse_kost)

    def set_status(self, status):
        """Stelt de status in. Enkel de waarden in STATUSSEN zijn toegelaten."""
        if status not in Vragenlijst.STATUSSEN:
            raise ValueError(f"Ongeldige status '{status}'. "
                             f"Kies uit: {', '.join(Vragenlijst.STATUSSEN)}.")
        self.__status = status

    # Extra methoden

    def dagen_tot_einddatum(self):
        """Geeft het aantal dagen tot de einddatum terug (None als er geen einddatum is).

        Een negatief getal betekent dat de einddatum al voorbij is.
        """
        if not self.__einddatum:
            return None
        return (self.__einddatum - date.today()).days

    def vervalt_binnen(self, aantal_dagen):
        """Geeft True als de licentie actief is en binnen aantal_dagen vervalt."""
        dagen = self.dagen_tot_einddatum()
        return (self.__status == "actief" and dagen is not None
                and 0 <= dagen <= aantal_dagen)

    def details(self):
        """Geeft alle gegevens van de vragenlijst terug als tekst over meerdere regels."""
        leverancier = self.__leverancier_naam or f"leverancier {self.__leverancier_id}"
        return (f"  Id:              {self.__id}\n"
                f"  Naam:            {self.__naam}\n"
                f"  Leverancier:     {leverancier}\n"
                f"  Afdeling:        {self.__afdeling}\n"
                f"  Contactpersoon:  {self.__contactpersoon or '-'}\n"
                f"  Status:          {self.__status}\n"
                f"  Startdatum:      {datum_als_tekst(self.__startdatum)}\n"
                f"  Einddatum:       {datum_als_tekst(self.__einddatum)}\n"
                f"  Opstartkost:     {kost_als_tekst(self.__opstartkost)} euro\n"
                f"  Jaarlijkse kost: {kost_als_tekst(self.__jaarlijkse_kost)} euro")

    def __str__(self):
        leverancier = self.__leverancier_naam or f"leverancier {self.__leverancier_id}"
        contactpersoon = self.__contactpersoon or "geen contactpersoon"
        periode = (f"{datum_als_tekst(self.__startdatum)} tot "
                   f"{datum_als_tekst(self.__einddatum)}")
        return (f"[{self.__id}] {self.__naam} ({leverancier}) - {self.__afdeling} - "
                f"{contactpersoon} - {self.__status} - {periode}")


if __name__ == "__main__":
    womac = Vragenlijst("WOMAC", 1, "Orthopedie", "An Peeters",
                        "01-01-2024", "31-12-2026", 250, 900, "actief",
                        vragenlijst_id=1, leverancier_naam="Mapi Research Trust (ePROVIDE)")
    hip = Vragenlijst("Oxford Hip Score", 2, "Orthopedie")
    print(womac)
    print(hip)
    print("Dagen tot einddatum WOMAC:", womac.dagen_tot_einddatum())
    print("Vervalt WOMAC binnen 60 dagen?", womac.vervalt_binnen(60))
    print("Einddatum WOMAC voor de database:", datum_voor_database(womac.get_einddatum()))
    print(womac.details())

    # De status wijzigen via de setter
    hip.set_status("actief")
    print("Nieuwe status Oxford Hip Score:", hip.get_status())

    # Testen van de controles
    try:
        hip.set_status("verlopen")
    except ValueError as fout:
        print("Fout opgevangen:", fout)

    try:
        hip.set_periode("01-01-2027", "01-01-2026")
    except ValueError as fout:
        print("Fout opgevangen:", fout)

    try:
        hip.set_periode("31/12/2026", None)
    except ValueError as fout:
        print("Fout opgevangen:", fout)

    try:
        hip.set_kosten(-5, None)
    except ValueError as fout:
        print("Fout opgevangen:", fout)
