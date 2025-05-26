# project/main_console.py
import datetime

from utils import berechne_alter, berechne_insulinmenge
from fhir_client import lese_patient_von_server
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Erstellung der Datenbank---
Base = declarative_base()

class MedApplication(Base):
    __tablename__ = 'medicationapplication'
    id = Column(Integer, primary_key=True)
    ingredient_name = Column(String(100), nullable=False)
    timestamp = Column(default=datetime.datetime.utcnow, nullable=False)
    bs_value = Column(Integer, nullable=False)
    broteinheiten = Column(Integer)

engine = create_engine('sqlite:///medications.db')
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

def erfasse_stammdaten():
    print("Bitte geben Sie die Patienteninformationen ein:")
    name = input("Name: ")
    geburtsdatum = input("Geburtsdatum (YYYY-MM-DD): ")
    return {"name": name, "geburtsdatum": geburtsdatum}

def erfasse_blutzuckerwerte():
    while True:
        try:
            blutzucker = int(input("Blutzuckerwert (mg/dL): "))
            broteinheiten = float(input("Broteinheiten: "))
            return blutzucker, broteinheiten
        except ValueError:
            print("Ungültige Eingabe. Bitte erneut versuchen.")

def main():
    print("--- Patientenverwaltung (Konsole) ---")
    stammdaten = erfasse_stammdaten()
    blutzucker, broteinheiten = erfasse_blutzuckerwerte()

    alter = berechne_alter(stammdaten['geburtsdatum'])
    insulin, bemerkung = berechne_insulinmenge(blutzucker, broteinheiten)

    print(f"\nPatient: {stammdaten['name']}, Alter: {alter} Jahre")
    print(f"Empfohlene Insulinmenge: {insulin} Einheiten")
    print(f"Hinweis: {bemerkung}")

    print("\n--- Daten vom FHIR-Server laden ---")
    patient = lese_patient_von_server("593210")
    if patient:
        print(f"FHIR-Patient: {patient['name']} ({patient['birthDate']})")

if __name__ == "__main__":
    main()
