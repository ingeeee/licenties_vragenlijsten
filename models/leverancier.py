"""Bevat de klasse leverancier"""


class Leverancier:
    """Een leverancier van licenties voor vragenlijsten."""

    def __init__(self, naam, email=None, leverancier_id=None):
        self.__id = leverancier_id
        self.set_naam(naam)
        self.set_email(email)

    def get_id(self):
        """Geeft de id van de leverancier terug (None als de leverancier nog niet is opgeslagen)."""
        return self.__id

    def get_naam(self):
        """Geeft de naam van de leverancier terug."""
        return self.__naam

    def set_naam(self, naam):
        """Stelt de naam van de leverancier in. De naam mag niet leeg zijn."""
        if not naam or not naam.strip():
            raise ValueError("De naam van de leverancier mag niet leeg zijn.")
        self.__naam = naam.strip()

    def get_email(self):
        """Geeft het e-mailadres van de leverancier terug (None als er geen e-mailadres is)."""
        return self.__email

    def set_email(self, email):
        """Stelt het e-mailadres in.

        Het e-mailadres mag leeg zijn, maar als het niet leeg is,
        moet het een geldig e-mailadres zijn."""
        if email and "@" not in email:
            raise ValueError(f"Het e-mailadres '{email}' is geen geldig e-mailadres.")
        self.__email = email if email else None

    def __str__(self):
        email = self.__email if self.__email else "geen e-mailadres"
        return f"[{self.__id}] {self.__naam} - {email}"


if __name__ == "__main__":
    leverancier1 = Leverancier("Oxford University Innovation", "licenties@voorbeeld-oxford.org", 2)
    leverancier2 = Leverancier("PROM Solutions BV", leverancier_id=3)
    print(leverancier1)
    print(leverancier2)

    try:
        Leverancier("Foute leverancier", "geen-emailadres")
    except ValueError as fout:
        print("Fout opgevangen:", fout)
