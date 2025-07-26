from fastapi import FastAPI, Path, HTTPException
import json
app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
        return data

@app.get("/")
def hello():
    return {"name" : "Patient management system API"}

@app.get("/info")
def info():
    return {"info" : "A fully functional API to manage your patients"}

@app.get("/view")
def view():
    data = load_data()
    return data

# Path is added to increase readibility
@app.get("/patient/{patient_id}")
def view_patient(patient_id: str  = Path(...,description="ID of the patient in DB", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail = "Patient not found")