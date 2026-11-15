# licenties_vragenlijsten
Een command line applicatie (CLI) om licenties voor vragenlijsten te beheren.

## Doel

In een ziekenhuis gebruiken verschillende afdelingen vragenlijsten (PROMs) waarvoor een licentie nodig is. Die licenties verlopen via verschillende leveranciers of individuele personen (auteurs van wetenschappelijke artikels).

Met deze tool houd je in één overzicht bij:

- Welke vragenlijsten er in gebruik zijn of aangevraagd werden, en bij welke leverancier.
- Voor welke afdeling de vragenlijst gebruikt en wie de interne contactpersoon is.
- De looptijd (start- en einddatum) en de kosten (eenmalige opstartkost en jaarlijkse kost).
- De status: aanvraag lopende, actief of opgezegd.

Zo zie je snel welke licenties binnenkort vervallen, wat elke afdeling jaarlijks betaalt, en kan je bij het vertrek van een collega al zijn of haar licenties in één keer overdragen.

## Functionaliteiten

Het hoofdmenu:

| Keuze | Functionaliteit |
|---|---|
| **Bekijken** | |
| 1 | Alle leveranciers tonen |
| 2 | Alle vragenlijsten tonen |
| 3 | Alle details van één vragenlijst bekijken, ook de kosten |
| 4 | Vragenlijsten zoeken op afdeling, leverancier, contactpersoon of status |
| 5 | Actieve licenties tonen die binnen een opgegeven aantal dagen vervallen |
| **Toevoegen** | |
| 6 | Een nieuwe leverancier toevoegen |
| 7 | Een nieuwe vragenlijst (of aanvraag) toevoegen |
| **Wijzigen** | |
| 8 | Een vragenlijst aanpassen: naam, leverancier, afdeling, contactpersoon, status, periode of kosten |
| 9 | Alle vragenlijsten van een contactpersoon overdragen aan een andere (bestaande of nieuwe) collega |
| **Rapport** | |
| 10 | Een rapport maken als csv-bestand: alle vragenlijsten, of de kosten per afdeling |

Enkele kenmerken:

- **Controle bij invoer:** elk veld wordt meteen gecontroleerd. Een lege naam, een ongeldige datum, een einddatum vóór de startdatum, een negatieve kost of een dubbele leverancier worden geweigerd, met een duidelijke melding.
- **Belgische notatie:** datums worden ingegeven en getoond als `DD-MM-JJJJ` (bv. `31-12-2026`), bedragen met een komma (bv. `1200,50`). In de database worden datums bewaard als `JJJJ-MM-DD`, zodat sorteren en vergelijken correct werkt.
- **Aanpassen:** bij het aanpassen zie je de huidige waarde tussen haakjes. Enter behoudt de huidige waarde, een `-` maakt een veld leeg. Wijzigingen worden pas opgeslagen als je daarvoor kiest, annuleren is altijd mogelijk.
- **Rapporten:** de csv-bestanden gebruiken een puntkomma als scheidingsteken en UTF-8-codering, zodat ze meteen correct openen in een Belgische versie van Excel. Het rapport van alle vragenlijsten bevat ook het aantal dagen tot de einddatum van elke actieve licentie.

## Installatie en ingebruikname

### Vereisten

- Python 3.10 of hoger (ontwikkeld met Python 3.14).
- Git.

### De repository klonen

```bash
git clone https://github.com/ingeeee/licenties_vragenlijsten.git
cd licenties_vragenlijsten
```

### Een virtuele omgeving maken en activeren

```bash
python -m venv .venv
```

Activeren:

*Windows (Git Bash)*
```bash
source .venv/Scripts/activate
```

*Windows (opdrachtprompt)*
```
.venv\Scripts\activate.bat
```

*Linux / macOS*
```bash
source .venv/bin/activate
```

### De packages installeren

```bash
pip install -r requirements.txt
```

De applicatie gebruikt het package `environs` om het instellingenbestand in te lezen.

### Het instellingenbestand aanmaken

De instellingen staan in een bestand `.env` in de hoofdmap van het project. Dit bestand zit niet in de repository. Maak het aan door het voorbeeldbestand te kopiëren:

```bash
cp .env.example .env        # Git Bash, Linux, macOS
```
```
copy .env.example .env      # Windows-opdrachtprompt
```

Opbouw van het instellingenbestand:

```
DB_PATH=data/licenties_vragenlijsten.db
RAPPORT_MAP=rapporten
```

| Instelling | Betekenis | Standaard |
|---|---|---|
| `DB_PATH` | Pad naar de SQLite-database. Relatief ten opzichte van de projectmap, of een volledig pad (bv. `C:/databases/licenties.db`). | verplicht |
| `RAPPORT_MAP` | Map waarin de csv-rapporten worden opgeslagen. | `rapporten` |

De mappen voor de database en de rapporten worden automatisch aangemaakt als ze nog niet bestaan.

### De database plaatsen

- **De meegeleverde voorbeelddatabase gebruiken:** plaats het bestand `licenties_vragenlijsten.db` op de locatie uit `DB_PATH`. Met de standaardinstelling is dat de map `data` in de projectmap: `data/licenties_vragenlijsten.db`.
- **Zelf een voorbeelddatabase aanmaken:** voer dit script uit. Het maakt de tabellen aan en vult ze met fictieve voorbeeldgegevens (alleen als de database nog leeg is):

  ```bash
  python maak_voorbeelddatabase.py
  ```

Start je de applicatie met een database die nog niet bestaat, dan worden de tabellen automatisch aangemaakt en begin je met een lege database.

### De applicatie starten

Start de applicatie vanuit de projectmap:

```bash
python main.py
```

Afsluiten kan met keuze `0` in het hoofdmenu (of met Ctrl+C).

## Database

De SQLite-database bevat 2 tabellen:

**leveranciers**

| Kolom | Type | Opmerking |
|---|---|---|
| id | INTEGER | primaire sleutel |
| naam | TEXT | verplicht, uniek |
| email | TEXT | optioneel |

**vragenlijsten**

| Kolom | Type | Opmerking |
|---|---|---|
| id | INTEGER | primaire sleutel |
| naam | TEXT | verplicht |
| leverancier_id | INTEGER | verwijst naar `leveranciers.id` |
| afdeling | TEXT | verplicht |
| contactpersoon | TEXT | optioneel |
| startdatum | TEXT | optioneel, `JJJJ-MM-DD` |
| einddatum | TEXT | optioneel, `JJJJ-MM-DD` |
| opstartkost | REAL | optioneel |
| jaarlijkse_kost | REAL | optioneel |
| status | TEXT | `aanvraag lopende`, `actief` of `opgezegd` |

Eén leverancier kan meerdere vragenlijsten hebben.

## Structuur van het project

```
licenties_vragenlijsten/
├── main.py                    # startpunt: het hoofdmenu
├── maak_voorbeelddatabase.py  # maakt een database met voorbeeldgegevens
├── .env.example               # voorbeeld van het instellingenbestand
├── requirements.txt           # benodigde packages
├── config/
│   └── config.py              # leest de instellingen uit .env
├── models/
│   ├── leverancier.py         # klasse Leverancier
│   ├── vragenlijst.py         # klasse Vragenlijst
│   └── omzetting.py           # controle en omzetting van datums en bedragen
├── services/
│   ├── database.py            # aanmaken van de tabellen
│   ├── leveranciers.py        # opzoekingen en toevoegen van leveranciers
│   ├── vragenlijsten.py       # opzoekingen, toevoegen en wijzigen van vragenlijsten
│   └── rapporten.py           # csv-rapporten
└── menu/
    ├── invoer.py              # hulpfuncties voor invoer en uitvoer in de terminal
    └── opties.py              # de functies achter elke keuze in het hoofdmenu
```

De verschillende onderdelen hebben elk hun eigen taak:

- `models` bevat de **domeinklassen**. Ze controleren zelf hun gegevens via setters.
- `services` bevat alle code die met de **database** of met **bestanden** werkt.
- `menu` bevat alle **interactie met de gebruiker** in de terminal.

De modules hebben elk een testblok (`if __name__ == "__main__":`). Die kan je vanuit de projectmap uitvoeren met de optie `-m`, bijvoorbeeld:

```bash
python -m models.vragenlijst
python -m services.vragenlijsten
```

## Opmerkingen over de voorbeeldgegevens

De namen van de leveranciers en de vragenlijsten bestaan echt. De contactpersonen, e-mailadressen, datums en bedragen zijn fictief.
