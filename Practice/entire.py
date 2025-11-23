from fastapi import FastAPI, Path, Query, HTTPException
import json
from typing import Annotated, Optional, Literal
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
app = FastAPI()

class Patient(BaseModel):
    id : Annotated[str, Field(..., description="Name of the person")]
    name: str
    city: str
    age: Annotated[int, Field(..., gt=0, lt=100)]
    gender: Literal['male', 'female', 'others']
    height: float
    weight: float

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
            return "Overweight"
        else:
            return "Obese"

def load_data():
    with open("../patients.json", 'r') as f:
        data = json.load(f)
        return data
    
def save_data(data):
    with open("../patients.json", 'w') as f:
        json.dump(data, f)

@app.get("/")
def home():
    return "This is the home page"

@app.get("/view")
def view_records():
    data = load_data()
    return data

@app.get("/sort")
def sort_patients(sort_by : str = Query(...,description="Sort based on Height, weight or BMI"), order: str = Query('asc', description="sort in asc or desc")):
    allowed_fields = ['height', 'weight', 'bmi']
    
    if sort_by not in allowed_fields:
        raise HTTPException(status_code=400, detail=f"The field you have selected is not valid, please select among {allowed_fields}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Choose among asc, desc")
    
    order_flag = True if order == 'desc' else False

    data = load_data()
    sorted_data = sorted(data.values(), key = lambda x : x.get(sort_by, 0), reverse = order_flag)
    return sorted_data

@app.create("/create")
def create_patient(patient: Patient):
    pass