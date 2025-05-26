import datetime

def berechne_alter(geburtsdatum_str):
    geburtsdatum = datetime.datetime.strptime(geburtsdatum_str, "%Y-%m-%d").date()
    heute = datetime.date.today()
    alter = heute.year - geburtsdatum.year - ((heute.month, heute.day) < (geburtsdatum.month, geburtsdatum.day))
    return alter

def berechne_insulinmenge(blutzucker, broteinheiten, relation=1.5):
    bemerkung = ""
    zusatz_insulin = broteinheiten * relation

    if blutzucker < 70:
        bemerkung = "Hypoglykämie! Bitte Glukose zu sich nehmen."
        return 0, bemerkung
    elif 70 <= blutzucker <= 199:
        bemerkung = "Normbereich. Nur mahlzeitenbedingtes Insulin notwendig."
        return zusatz_insulin, bemerkung
    elif blutzucker >= 200:
        korrektur = (blutzucker - 100) / 50
        gesamt = korrektur + zusatz_insulin
        bemerkung = "Zusätzliches Korrekturinsulin notwendig."
        return gesamt, bemerkung
    return 0, "Keine Berechnung möglich."
