from fastapi import FastAPI, Path, HTTPException
import json
app = FastAPI()

def load_data():
    with open('../patients.json', 'r') as f:
        data = json.load(f)
        return data

@app.get("/")
def home():
    return "This is home"

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def get_patient(patient_id: str = Path(..., description="Id of the patient to find in DB", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")
