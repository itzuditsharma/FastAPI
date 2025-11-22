from fastapi import FastAPI, Path, Query, HTTPException
import json
app = FastAPI()

def load_data():
    with open("../patients.json", 'r') as f:
        data = json.load(f)
        return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id : str = Path(..., description="ID of patient")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient detail not found")

@app.get('/sort')
def sort_patients(sort_by: str = Query(...,description="Sort on basis of height, weight or BMI"), order: str = Query('asc', description="sort in asc or desc")):
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail = f"invalid field selected, select from {valid_fields}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order select, select from asc, desc")
    
    data = load_data()

    sort_order = True if order == 'desc' else False

    print("#######This is Data#######")
    print(data)

    print("########Data Values##########")
    print(data.values())

    sorted_data = sorted(data.values(), key = lambda x : x.get(sort_by, 0), reverse=sort_order)

    return sorted_data