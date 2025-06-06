import datetime

# https://build.fhir.org/medicationdispense0302.json.html

# Patientenstammdaten einmalig erfassen
def erfasse_stammdaten():
    print("\nBitte geben Sie die Patientenstammdaten ein:")
    name = input("Name: ")
    vorname = input("Vorname: ")
    geburtsdatum = input("Geburtsdatum (TT.MM.JJJJ): ")
    geschlecht = input("Geschlecht (weiblich/männlich/divers): ")
    adresse = input("Adresse: ")    
    insulinart = input("Insulinart: ")
    alter = berechne_alter(geburtsdatum)
    return {"name": name, "vorname": vorname, "alter": alter, "geschlecht": geschlecht, "adresse": adresse,
            "insulinart": insulinart}

# Alter berechnen
def berechne_alter(geburtsdatum):
    heute = datetime.date.today()
    geburtsdatum_dt = datetime.datetime.strptime(geburtsdatum, "%d.%m.%Y").date()
    alter = heute.year - geburtsdatum_dt.year - (
                (heute.month, heute.day) < (geburtsdatum_dt.month, geburtsdatum_dt.day))
    return alter

# Insulinschema einmalig festlegen
def erfasse_insulinschema(insulinart):
    print("\nBitte geben Sie das Insulinschema ein:")
    return {
        (200, 250): {"insulinart": insulinart, "ie": input("IE bei Blutzucker 200-250 mg/dl: ")},
        (251, 300): {"insulinart": insulinart, "ie": input("IE bei Blutzucker 251-300 mg/dl: ")},
        (301, 350): {"insulinart": insulinart, "ie": input("IE bei Blutzucker 301-350 mg/dl: ")},
        (351, 400): {"insulinart": insulinart, "ie": input("IE bei Blutzucker 351-400 mg/dl: ")},
        (401, 800): {"insulinart": insulinart, "ie": input("IE bei Blutzucker 401-800 mg/dl: ")},
    }
# Abfrage der BE-Insulinrelation
def erfasse_be_insulin_relation():
    return float(input("\nWie viele Insulin-Einheiten (IE) werden pro 1 BE gespritzt?: "))

# Insulinbedarf berechnen
def berechne_insulinmenge(blutzuckerwert, insulinschema, be_insulin_relation, broteinheiten):
    if blutzuckerwert < 70:
        return "Bitte Glucose einnehmen oder Essen zu sich nehmen!", None
    elif 71 <= blutzuckerwert <= 199:
        zusatz_insulin = broteinheiten * be_insulin_relation
        return f"Blutzuckerwert im Bereich 71-199 mg/dl. BE-abhängige Insulinmenge: {zusatz_insulin} IE", zusatz_insulin
    elif blutzuckerwert >= 200:
        for wertgrenze, menge in insulinschema.items():
            if wertgrenze[0] <= blutzuckerwert <= wertgrenze[1]:
                basis_insulin = float(menge['ie'])
                zusatz_insulin = broteinheiten * be_insulin_relation if blutzuckerwert > 71 else 0
                gesamt_insulin = basis_insulin + zusatz_insulin
                return f"Insulinart: {menge['insulinart']}, Gesamt-IE: {gesamt_insulin} (Basis: {basis_insulin}, Zusatz: {zusatz_insulin})", gesamt_insulin
    return "Kein Insulin erforderlich.", None

# Hauptprogramm
print("Patientenverwaltung gestartet.")
stammdaten = erfasse_stammdaten()
insulinschema = erfasse_insulinschema(stammdaten["insulinart"])
be_insulin_relation = erfasse_be_insulin_relation()

while True:
    print(f"\nPatient: {stammdaten['name']} {stammdaten['vorname']}, Alter: {stammdaten['alter']} Jahre")
    blutzuckerwert = int(input("Bitte aktuellen Blutzuckerwert eingeben: "))
    broteinheiten = float(input("Wie viele Broteinheiten (BE) werden eingenommen?: "))

    # Abfrage zur BE-Insulinrelation
    be_ändern = input("Möchten Sie die BE-Insulinrelation ändern? (ja/nein): ").strip().lower()
    if be_ändern == "ja":
        be_insulin_relation = erfasse_be_insulin_relation()

    empfohlene_insulinmenge, gesamt_insulin = berechne_insulinmenge(blutzuckerwert, insulinschema, be_insulin_relation,
                                                                    broteinheiten)
    print(empfohlene_insulinmenge)


    erneuern = input("\nMöchten Sie das Insulinschema ändern? (ja/nein): ").strip().lower()
    if erneuern == "ja":
        insulinschema = erfasse_insulinschema(stammdaten["insulinart"])
