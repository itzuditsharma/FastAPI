from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json
app = FastAPI()


# gt = greater than 
# lt = lesser than 
class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples = ["P001"])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City where Patient lives")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Normal"
        else:
            return "Obese"
    
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
        return data
    
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

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
# http://127.0.0.1:8000/patient/P001
@app.get("/patient/{patient_id}")
def view_patient(patient_id: str  = Path(...,description="ID of the patient in DB", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail = "Patient not found")

# http://127.0.0.1:8000/sort?sort_by=height&order=desc
@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):
    # load the existing data 
    data = load_data()

    # Check if user already present 
    if patient.id in data:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # add new patient to database 
    # model.dump -> converts data from pydantic object to dictionary  
    data[patient.id] = patient.model_dump(exclude=['id'])

    # Save into json file 
    save_data(data)

    return JSONResponse(status_code=201, content={"message" : "Patient created successfully"})