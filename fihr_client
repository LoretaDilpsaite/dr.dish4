from fhirclient import client
import fhirclient.models.patient as p

settings = {
    'app_id': 'FHIR_Application',
    'api_base': 'https://hapi.fhir.org/baseR4'
}

smart = client.FHIRClient(settings=settings)

def lese_patient_von_server(patient_id):
    try:
        patient = p.Patient.read(patient_id, smart.server)
        name = f"{patient.name[0].given[0]} {patient.name[0].family}"
        geburtsdatum = patient.birthDate.isostring
        return {"name": name, "birthDate": geburtsdatum}
    except Exception as e:
        print(f"Fehler beim Abrufen des Patienten: {e}")
        return None
